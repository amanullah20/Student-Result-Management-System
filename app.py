
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


# -------- Database --------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Students
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT
    )
    """)

    # Subjects
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT
    )
    """)

    # Marks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        marks REAL
    )
    """)

    conn.commit()
    conn.close()



# -------- Grade --------
def get_grade(avg):
    if avg >= 80:
        return "A+"
    elif avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 33:
        return "D"
    else:
        return "F"


# -------- Login --------
@app.route('/', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['user'] = username
            return redirect('/dashboard')

    return render_template("login.html")


# -------- Dashboard --------
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    if request.method == 'POST':

        name = request.form['name']
        roll = request.form['roll']

        # Save Student
        cursor.execute("INSERT INTO students(name, roll) VALUES(?,?)",(name,roll))
        student_id = cursor.lastrowid

        # Save Marks
        for subject in subjects:
            mark = request.form[str(subject[0])]
            cursor.execute(
                "INSERT INTO marks(student_id, subject_id, marks) VALUES(?,?,?)",
                (student_id, subject[0], mark)
            )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    conn.close()
    return render_template("index.html", subjects=subjects)



# -------- History --------
@app.route('/history')
def history():

    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results")
    data = cursor.fetchall()

    conn.close()

    return render_template("history.html", data=data)


# -------- Logout --------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):

    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM results WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/history')


@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):

    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        roll = request.form['roll']

        bangla = float(request.form['bangla'])
        english = float(request.form['english'])
        math = float(request.form['math'])
        ict = float(request.form['ict'])
        physics = float(request.form['physics'])
        chemistry = float(request.form['chemistry'])

        total = bangla + english + math + ict + physics + chemistry
        average = round(total / 6, 2)

        grade = get_grade(average)

        if all(mark >= 33 for mark in [bangla, english, math, ict, physics, chemistry]):
            result = "PASS"
        else:
            result = "FAIL"

        cursor.execute("""
        UPDATE results
        SET name=?, roll=?, bangla=?, english=?, math=?, ict=?, physics=?, chemistry=?, average=?, grade=?, result=?
        WHERE id=?
        """,(name,roll,bangla,english,math,ict,physics,chemistry,average,grade,result,id))

        conn.commit()
        conn.close()

        return redirect('/history')

    cursor.execute("SELECT * FROM results WHERE id=?", (id,))
    data = cursor.fetchone()

    conn.close()

    return render_template("edit.html", data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():

    if 'user' not in session:
        return redirect('/')

    data = None

    if request.method == 'POST':
        roll = request.form['roll']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM results WHERE roll=?", (roll,))
        data = cursor.fetchall()

        conn.close()

    return render_template("search.html", data=data)



@app.route('/chart')
def chart():

    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Pass / Fail Count
    cursor.execute("SELECT result, COUNT(*) FROM results GROUP BY result")
    result_data = cursor.fetchall()

    pass_count = 0
    fail_count = 0

    for row in result_data:
        if row[0] == "PASS":
            pass_count = row[1]
        else:
            fail_count = row[1]

    # Grade Count
    cursor.execute("SELECT grade, COUNT(*) FROM results GROUP BY grade")
    grade_data = cursor.fetchall()

    conn.close()

    grades = [row[0] for row in grade_data]
    grade_count = [row[1] for row in grade_data]

    return render_template(
        "chart.html",
        pass_count=pass_count,
        fail_count=fail_count,
        grades=grades,
        grade_count=grade_count
    )

@app.route('/pdf/<int:id>')
def generate_pdf(id):

    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results WHERE id=?", (id,))
    student = cursor.fetchone()

    conn.close()

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Student Marksheet", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Name: {student[1]}", styles['Normal']))
    content.append(Paragraph(f"Roll: {student[2]}", styles['Normal']))
    content.append(Spacer(1, 15))

    content.append(Paragraph(f"Bangla: {student[3]}", styles['Normal']))
    content.append(Paragraph(f"English: {student[4]}", styles['Normal']))
    content.append(Paragraph(f"Math: {student[5]}", styles['Normal']))
    content.append(Paragraph(f"ICT: {student[6]}", styles['Normal']))
    content.append(Paragraph(f"Physics: {student[7]}", styles['Normal']))
    content.append(Paragraph(f"Chemistry: {student[8]}", styles['Normal']))

    content.append(Spacer(1, 15))

    content.append(Paragraph(f"Average: {student[9]}", styles['Normal']))
    content.append(Paragraph(f"Grade: {student[10]}", styles['Normal']))
    content.append(Paragraph(f"Result: {student[11]}", styles['Normal']))

    doc.build(content)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="marksheet.pdf",
        mimetype='application/pdf'
    )

@app.route('/add_subject', methods=['GET','POST'])
def add_subject():

    if request.method == 'POST':
        subject = request.form['subject']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO subjects(subject_name) VALUES(?)",(subject,))
        conn.commit()
        conn.close()

        return redirect('/add_subject')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    conn.close()

    return render_template("add_subject.html", subjects=subjects)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=500, debug=True)

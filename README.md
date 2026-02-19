 

# 🎓 Student Result Management System (Flask)

A dynamic web-based student result management system built using **Flask**, **SQLite**, **Bootstrap**, and **Jinja2**.

This project allows admins to manage subjects, enter student marks dynamically, calculate average and grade automatically, and view result history with edit/delete options.

---

## 🚀 Features

- 🔐 Admin Login System
- ➕ Add Subjects Dynamically
- 📝 Dynamic Result Entry (Subjects auto-load from database)
- 📊 Automatic Average Calculation
- 🏆 Grade System (A+, A, B, C, F)
- ✅ Pass / Fail Detection
- 📂 Result History View
- ✏ Edit Student Result
- ❌ Delete Student Result
- 📈 Analytics Dashboard
- 📄 PDF Result Export (Optional Feature)

---

## 🛠 Technologies Used

- Python
- Flask
- SQLite
- HTML5
- Bootstrap 5
- Jinja2 Template Engine

---

## 📂 Project Structure

project-folder/
│
├── app.py
├── database.db
│
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── history.html
│ ├── add_subject.html
│ ├── edit.html
│ └── chart.html
│
└── static/
└── style.css 


---

## 🧠 How It Works

1. Admin logs in
2. Subjects are added from Add Subject page
3. Dashboard dynamically loads subjects
4. Admin enters student marks
5. System calculates:
   - Total Marks
   - Average
   - Grade
   - Pass/Fail
6. Data is stored in SQLite database
7. History page displays all results

---

## 🎯 Grade System Logic

| Average Marks | Grade |
|--------------|--------|
| 80+          | A+     |
| 70-79        | A      |
| 60-69        | B      |
| 50-59        | C      |
| Below 50     | F      |

Pass condition: Average ≥ 40

---

## ⚙ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/student-result-system.git
cd student-result-system
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies 

```bash
pip install flask
pip install reportlab 
```

### 4️⃣ Run the Application 

```bash
python app.py
``` 

Then open: 

```bash 
http://127.0.0.1:5000/

``` 

### 🗄 Database

The system uses SQLite database.

Main tables:

 - users

 - subjects

 - results 

### 📸 Screenshots

(Add screenshots of Dashboard, History page, Login page here) 


### 🌟 Future Improvements

- GPA Calculation System

- Student Profile Page

- Excel Export

- API Version

- Role-based Access (Admin/Teacher)

- Deployment on Render / Railway 

### 👨‍💻 Author

Aman Ullah
Developer
Portfolio Project 2026 

### 📜 License

This project is for educational and portfolio purposes.
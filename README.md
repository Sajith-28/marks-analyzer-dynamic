# Student Marks Analyzer – GitHub & Environment Configuration Task

## Project Overview

The **Student Marks Analyzer** is a dynamic **Streamlit-based Python application** that allows users to enter student names and marks (including negative values), calculate the average score, identify students scoring above average, and store all data permanently in **MongoDB** along with date and time.

As part of today’s task, this project was enhanced using **professional GitHub workflow practices** and **secure environment variable configuration**.

---

## 🎯 Task Given (Today)

### Task 1: GitHub Commands Using VS Code
- Work with an **existing GitHub repository**
- Learn and use basic Git commands inside **VS Code**
- Commit and push changes correctly

### Task 2: Configuration Using `.env`
- Store sensitive values such as:
  - MongoDB URL
  - Database name
  - Collection name
- Create a `config.py` file to access environment variables
- Learn:
  - How to create a `.env` file
  - How to store values inside `.env`
  - How to read environment variables in Python
  - How to prevent `.env` from being uploaded to GitHub using `.gitignore`

---

## ✅ What I Successfully Completed

### 🔹 GitHub (Task 1)
- Cloned an existing GitHub repository using VS Code
- Worked inside the correct Git-tracked project folder
- Used Git commands:
  - `git status`
  - `git add .`
  - `git commit`
  - `git push`
- Successfully pushed changes to the `main` branch

### 🔹 Environment Variables & Configuration (Task 2)
- Created a `.env` file to store sensitive configuration data
- Stored MongoDB credentials securely
- Created `config.py` to load environment variables
- Used environment variables inside the main application
- Added `.env` to `.gitignore`
- Verified that:
  - `.env` exists locally
  - `.env` is NOT visible on GitHub

This follows **industry-standard security practices**.

---

## 🔐 Project Structure
marks-analyzer-dynamic/
│
├── marks_analyzer.py # Main Streamlit application
├── config.py # Environment variable loader
├── .gitignore # Prevents pushing .env
├── .env # Environment variables (local only)
├── requirements.txt # Dependencies
├── README.md # Documentation
└── .git/ # Git repository data


---

## ✨ Application Features

- Dynamic input for **any number of students**
- Accepts **negative and large positive marks** (error correction)
- Automatically calculates **average marks**
- Displays **students scoring above average**
- Saves all data to **MongoDB**
- Stores **date and time** for each record
- Option to view **all previous records**

---

## 🧠 Application Algorithm

1. Connect to MongoDB using environment variables  
2. Ask user for number of students  
3. Dynamically generate input fields for student names and marks  
4. On clicking **Calculate & Save**:
   - Calculate the average mark  
   - Display students above average  
   - Save data to MongoDB with date & time  
5. Optionally display all previously stored records  

---

## ⚙️ Technologies Used

- Python  
- Streamlit  
- MongoDB  
- Git & GitHub  
- VS Code  
- python-dotenv  

---

## 💻 Program / Source Code

```python
import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# ---------------- MongoDB Connection ----------------
import config
client = MongoClient(config.MONGO_URL)
db = client[config.DB_NAME]
collection = db[config.COLLECTION_NAME]

st.success("Connected to MongoDB")

# ---------------- App Title ----------------
st.title("Student Marks Analyzer")
st.write("Enter student names and marks. Date and time are saved automatically.")

# ---------------- Number of Students ----------------
num_students = st.number_input(
    "How many students?",
    min_value=1,
    step=1
)

students = []

# ---------------- Input Section ----------------
for i in range(int(num_students)):
    name = st.text_input(f"Enter name of student {i + 1}")

    # Name validation (only alphabets)
    if name and not name.replace(" ", "").isalpha():
        st.error("Name must contain only alphabets")
        st.stop()

    mark = st.number_input(
        f"Enter mark of {name if name else 'Student ' + str(i + 1)}",
        min_value=None,      # Allows negative values
        max_value=100.0,
        step=1.0
    )

    students.append({
        "name": name if name else f"Student {i + 1}",
        "mark": mark
    })

# ---------------- Calculate & Save ----------------
if st.button("Calculate & Save"):
    marks = [s["mark"] for s in students]
    average = sum(marks) / len(marks)

    st.subheader(f"Average Mark: {average:.2f}")
    st.write("Students above average:")

    above_avg = False
    for s in students:
        if s["mark"] > average:
            st.write(f"{s['name']} : {s['mark']}")
            above_avg = True

    if not above_avg:
        st.info("No student scored above average")

    document = {
        "students": students,
        "average": average,
        "created_at": datetime.utcnow()
    }

    collection.insert_one(document)
    st.success("Data saved with date and time")

# ---------------- Show Records ----------------
if st.checkbox("Show all saved records"):
    records = collection.find().sort("created_at", -1)

    for rec in records:
        created_time = rec["created_at"].strftime("%d-%m-%Y %I:%M %p")
        st.write("Date & Time:", created_time)
        st.write(f"Average: {rec['average']:.2f}")

        for s in rec["students"]:
            st.write(f"{s['name']} : {s['mark']}")

        st.write("--------------------------------")
```

## 📸 Output Screenshots

### 🖥️ Application Output
<img width="1068" height="1010" alt="image" src="https://github.com/user-attachments/assets/17d7b185-462a-4946-9ff1-863920c46e49" />

---

### 🗄️ MongoDB Records
<!-- Upload MongoDB records screenshot here -->
<img width="1742" height="976" alt="mm" src="https://github.com/user-attachments/assets/eaf53978-a6b7-4c9a-b60e-f22480b46a3d" />

---

### 🔐 `.env` File (Local Configuration)
<img width="1405" height="532" alt="image" src="https://github.com/user-attachments/assets/67a24611-da28-494b-9dce-2b57e7341207" />

---

### ⚙️ `config.py` File
<img width="1209" height="459" alt="image" src="https://github.com/user-attachments/assets/fcd03a6e-0cb2-4167-84a4-71557b133355" />

<img width="1236" height="451" alt="image" src="https://github.com/user-attachments/assets/8083ed12-832f-488f-bc52-8dea0e4e29d0" />

---

### 🌐 GitHub Repository View
<img width="1919" height="963" alt="image" src="https://github.com/user-attachments/assets/075efe83-078d-4210-830f-028e42ec73b1" />

## Conclusion

This project successfully demonstrates the development of a **dynamic and secure Student Marks Analyzer application** using **Python, Streamlit, and MongoDB**.

Through this task, I learned how to:
- Work professionally with an **existing GitHub repository**
- Use essential **Git commands** inside VS Code
- Securely manage sensitive data using **environment variables (`.env`)**
- Protect confidential information using **`.gitignore`**
- Integrate a Python application with **MongoDB**
- Build a dynamic, real-world web application using **Streamlit**

By separating configuration data from source code and following GitHub best practices, the project is now **secure, maintainable, and scalable**.  
This task strengthened my understanding of **version control, secure configuration management, database integration, and professional software development workflows**, making the application suitable for real-world usage.


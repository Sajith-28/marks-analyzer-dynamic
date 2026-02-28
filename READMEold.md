# Dynamic Student Marks Analyzer with MongoDB

A **Streamlit app** to input student names and marks (including negative values), calculate the average, identify students scoring above average, and save all data to **MongoDB**. Supports **error correction** scenarios.

---

## Features

- Input **any number of students** dynamically.  
- Enter **student names** and **marks** (supports negative and large positive values).  
- Calculates **average mark** automatically.  
- Shows **students scoring above average**.  
- **Saves data to MongoDB** (`AVG` database, `STU` collection).  
- Optionally displays **all previous records**.  

---

## Algorithm

1. Connect to MongoDB (`AVG` database, `STU` collection).  
2. Take input for the **number of students**.  
3. Dynamically generate input fields for **student names and marks**.  
4. When the **Calculate & Save** button is clicked:  
   - Compute the **average mark**.  
   - Display **students with marks above average**.  
   - Save the **student data and average** to MongoDB.  
5. Optional: Display all **previous records** stored in MongoDB.  

---

## Installation & Usage
```
git clone https://github.com/your-username/dynamic-student-marks.git
cd dynamic-student-marks
```
## Install dependencies:
```
pip install streamlit pymongo
streamlit run marks_analyzer.py
```

## Program / Code

```python
import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# ---------------- MongoDB Connection ----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["AVG"]
collection = db["STU"]

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

    # 🔴 Name validation (only alphabets)
    if name and not name.replace(" ", "").isalpha():
        st.error("Name must contain only alphabets")
        st.stop()

    mark = st.number_input(
        f"Enter mark of {name if name else 'Student ' + str(i + 1)}",
        min_value=None,     # ✅ Allows negative marks
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

    st.subheader("Average Mark: {:.2f}".format(average))

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
        st.write("Date & Time: " + created_time)
        st.write("Average: {:.2f}".format(rec["average"]))

        for s in rec["students"]:
            st.write(f"{s['name']} : {s['mark']}")

        st.write("--------------------------------")
)
```

## Sample Output

1. Enter 2 students:  
   - sajith: -90.00
   - raju: 40.00 

**Output Screenshot:**  

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/f8d86973-d8f4-4084-96a2-a5384af30372" />

**Mongo DB entry:**
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/8d50e2f7-06dc-4f93-a6e6-6f72a7ee67f8" />

---

## Conclusion

The **Student Marks Analyzer** app is a dynamic tool that allows:  

- Inputting any number of student marks, including **negative values** for **error correction**.  
- Calculating the **average mark** and identifying students who scored above average.  
- Saving all data to **MongoDB** for persistent storage and future reference.  
- Viewing all **previous records** directly within the app.  

### Benefits of Error Correction

- Supports **correction of input mistakes**, such as negative or unusually high marks.  
- Helps teachers/admins **validate data** before final reporting.  
- Improves accuracy and reliability of student performance analysis.  

### Personal Learning Outcomes

While building this project, I learned:  

- How to use **Streamlit** to create dynamic web apps.  
- How to **connect and store data in MongoDB** from Python.  
- How to handle **user input errors** and make the app robust for real-world scenarios.  
- How to calculate and analyze **statistics dynamically** for multiple students.  

This project strengthened my understanding of **Python, web app design, databases, and data validation**, while creating a **practical tool for real-world use**.

---


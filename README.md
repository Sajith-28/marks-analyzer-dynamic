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

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["AVG"]
collection = db["STU"]
st.write("Connected to MongoDB ")

st.title("Student Marks Analyzer (Fully Dynamic for Error Correction)")
st.write("Enter the names and marks of students (minimum 1 student).")

# Number of students
num_students = st.number_input("How many students?", min_value=1, step=1)

students = []

# Input names and marks
for i in range(int(num_students)):
    name = st.text_input(f"Enter name of student {i+1}:")
    mark = st.number_input(
        f"Enter mark of {name if name else f'Student {i+1}'}:", 
        value=0.0,
        step=1.0
    )
    students.append({"name": name if name else f"Student {i+1}", "mark": mark})

# Calculate average and save to MongoDB
if st.button("Calculate & Save"):
    if students:
        marks = [s["mark"] for s in students]
        average = sum(marks) / len(marks)
        st.subheader(f"Average Mark = {average:.2f}")

        st.write("### Students with marks above average:")
        found = False
        for s in students:
            if s["mark"] > average:
                st.write(f"{s['name']}: {s['mark']}")
                found = True
        if not found:
            st.write("No student scored above average.")

        document = {
            "students": students,
            "average": average
        }
        collection.insert_one(document)
        st.success("Marks and names saved to MongoDB ")

# Display all previous records
if st.checkbox("Show all previous records"):
    records = collection.find()
    for rec in records:
        st.write(f"Average: {rec['average']:.2f}")
        for s in rec["students"]:
            st.write(f"{s['name']}: {s['mark']}")
        st.write("---")
```

## Sample Output

1. Enter 3 students:  
   - Alice: 80  
   - Bob: -5  
   - Charlie: 70  

**Output Screenshot:**  

<img width="1915" height="1012" alt="image" src="https://github.com/user-attachments/assets/425debd6-9b6f-464f-a95f-c23632c9947d" />
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


import streamlit as st
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["AVG"]
collection = db["STU"]
st.write("Connected to MongoDB ")

st.title("Student Marks Analyzer (Fully Dynamic for Error Correction)")
st.write("Enter the names and marks of students (minimum 1 student).")

num_students = st.number_input("How many students?", min_value=1, step=1)

students = []

for i in range(int(num_students)):
    name = st.text_input(f"Enter name of student {i+1}:")
    mark = st.number_input(
        f"Enter mark of {name if name else f'Student {i+1}'}:", 
        value=0.0,      # default value
        step=1.0         # increment step
        # no min_value or max_value, so negatives and large positives allowed
    )
    students.append({"name": name if name else f"Student {i+1}", "mark": mark})

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
        st.success("Marks and names saved to MongoDB ✅")

if st.checkbox("Show all previous records"):
    records = collection.find()
    for rec in records:
        st.write(f"Average: {rec['average']:.2f}")
        for s in rec["students"]:
            st.write(f"{s['name']}: {s['mark']}")
        st.write("---")

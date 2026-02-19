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
        min_value=None,     # Allows negative marks
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

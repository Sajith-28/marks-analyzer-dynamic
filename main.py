from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

app = FastAPI()

# -------------------------------
# MongoDB SAFE connection
# -------------------------------
try:
    client = MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=3000  # prevents infinite loading
    )
    client.server_info()  # test connection
    db = client["school"]
    students_collection = db["students"]
    mongo_connected = True
except ServerSelectionTimeoutError:
    mongo_connected = False

# -------------------------------
# Models
# -------------------------------
class Student(BaseModel):
    name: str
    mark: float

class UpdateStudentRequest(BaseModel):
    name: str
    mark: float

# -------------------------------
# Routes
# -------------------------------
@app.get("/")
def home():
    return {"message": "FastAPI is running"}

@app.get("/test-mongo")
def test_mongo():
    if not mongo_connected:
        raise HTTPException(status_code=500, detail="MongoDB not connected")
    return {"message": "MongoDB connected successfully"}

@app.get("/students")
def get_students():
    if not mongo_connected:
        raise HTTPException(status_code=500, detail="MongoDB not connected")

    students = list(students_collection.find({}, {"_id": 0}))
    return students

@app.post("/students")
def add_student(student: Student):
    if not mongo_connected:
        raise HTTPException(status_code=500, detail="MongoDB not connected")

    students_collection.insert_one(student.dict())
    return {"message": "Student added successfully"}

@app.put("/students")
def update_student(data: UpdateStudentRequest):
    if not mongo_connected:
        raise HTTPException(status_code=500, detail="MongoDB not connected")

    result = students_collection.update_one(
        {"name": data.name},
        {"$set": {"mark": data.mark}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": f"{data.name} updated successfully"}

@app.delete("/students")
def delete_student(name: str):
    if not mongo_connected:
        raise HTTPException(status_code=500, detail="MongoDB not connected")

    result = students_collection.delete_one({"name": name})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": f"{name} deleted successfully"}
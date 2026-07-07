from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "Stephen", "course": "Computer Science"},
    {"id": 2, "name": "Alice", "course": "Business"}
]

@app.get("/")
def home():
    return {"message": "Welcome to Student API"}

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    return {"error": "Student not found"}

@app.post("/students")
def add_student(student: dict):
    students.append(student)
    return {
        "message": "Student added successfully",
        "student": student
    }



    
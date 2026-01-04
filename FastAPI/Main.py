from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def test():
    return {"message": "No more delays! get back on work!"}

@app.get("/test2")
def test2():
    return {"message": "This is test2 function."}

student={1:"Kamesh",2:"Ramesh",3:"Suresh"}
@app.get("/student/{student_id}")
def get_student(student_id: int):
    return {"student_name": student.get(student_id, "Student not found")}

def get_student_name(student_id: int):
    return student.get(student_id, "Student not found")

@app.get("/students/{student_id}/{student_name}")
def add_student(student_id: int, student_name: str):
    student[student_id] = student_name
    return student

@app.get("/add_student") 
def add_student_parameters(student_id: int, student_name: str):
    student[student_id] = student_name
    return student



@app.post("/add_student_post")
def add_student_post():
    student['student_id'] = 'student_name'
    return student


class StudentData(BaseModel):
    student_id: int
    student_name: str

@app.post("/add_student_pydantic")

def add_student_pydantic(newdata: StudentData):
    student[newdata.student_id] = newdata.student_name
    return student
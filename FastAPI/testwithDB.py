from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

db_url="postgresql://neondb_owner:npg_DqH1aJB2yjdt@ep-sweet-breeze-ad2b2zx1-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_connection():
    conn=psycopg2.connect(db_url,cursor_factory=RealDictCursor)
    return conn 

class StudentData(BaseModel):
    id:int
    name:str
    age:int


class StudentInputID(BaseModel):
    id:int


@app.post("/create_student")
def create_student(stud:StudentData):
    return stud


def save_student_file(data):
    with open("student.txt","a")as f:
        f.write(f"{data.id},{data.name},{data.age}\n")


@app.post("/stud_file")

def create_student_file(stud:StudentData):
    
    save_student_file(stud)
    return{"student data saved successfully"}

def read_student_file():
    students_read=[]
    if not os.path.exists("student.txt"):
        return students_read
    with open("student.txt","r")as f:
        for line in f:
            id,name,age= line.strip().split(",")
            students_read.append({

                "id":int(id),
                "name":name,
                "age":int(age)
            })
    return students_read


@app.get("/read_stud_file")
def show_student_file():
    students=read_student_file()

    if not students:
        return {"message":"no students found"}
    return students
    
@app.post("/student/insert_db")
def insert_data_db(stud:StudentData):
    conn=get_connection()
    cursor=conn.cursor()
    insert_query="INSERT INTO STUDENT(id,name,age) values(%s,%s,%s)"
    cursor.execute(insert_query,(stud.id,stud.name,stud.age))
    conn.commit()
    cursor.close()
    conn.close()
    return {"Student data inserted"}

@app.post("/student/update_db")
def update_data_db(stud:StudentData):
    conn=get_connection()
    cursor=conn.cursor()
    update_query="UPDATE STUDENT set name=%s,age=%s where id=%s"
    cursor.execute(update_query,(stud.name,stud.age,stud.id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"student data updated successfully"}


@app.post("/student/update_db/Parameter")
def update_data_db(sid:StudentInputID):
    conn=get_connection()
    cursor=conn.cursor()
    update_query="UPDATE STUDENT set name=%s,age=%s where id=%s"
    cursor.execute(update_query,("Parameter",25,sid.id,))
    if cursor.rowcount ==0:
     conn.commit()
     cursor.close()
     conn.close()
     return {" no rows found"}
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"student data updated successfully"}


@app.post("/student/delete_db/Parameter")
def delete_data_db(sid:StudentInputID):
    conn=get_connection()
    cursor=conn.cursor()
    delete_query="Delete from STUDENT where id=%s"
    cursor.execute(delete_query,(sid.id,))
    if cursor.rowcount ==0:
     conn.commit()
     cursor.close()
     conn.close()
     return {" no rows found"}
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"student data deleted successfully"}


@app.post("/student/select_db/Parameter")
def select_data_db(sid:StudentInputID):
    conn=get_connection()
    cursor=conn.cursor()
    select_query="SELECT id, name, age from STUDENT where id=%s"
    cursor.execute(select_query,(sid.id,))
    student=cursor.fetchone()
    cursor.close()
    conn.close()

    if student is None:
        return {"message": "Student not found in DB"}
    
    return student

import psycopg2
from models import Student
from fastapi import FastAPI,HTTPException
import os
import logging
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

conn = psycopg2.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    dbname=db_name
)
cur = conn.cursor()


app=FastAPI()

@app.post("/students")
def create_stud(student: Student):
    try:
        cur.execute(
            "INSERT INTO stud (id, name, section, cgpa) VALUES "
            "(%s, %s, %s, %s)",
            (student.id, student.name, student.section, student.cgpa)
        )
        conn.commit()
        return {"message": "Student saved", "data": student}
    except Exception:
        raise HTTPException(status_code=500, detail="Couldn't save student")
    
@app.get("/students/{roll_no}")
def get_student_by_roll(roll_no: int):
    try:
        cur.execute("SELECT * FROM stud WHERE id = %s;", (roll_no,))
        existing = cur.fetchone()
        
        if existing:
            return existing
        return {"message": "Student not found"}
    except Exception:
        raise HTTPException(status_code=500, detail="Couldn't fetch student")
@app.put("/students/{roll_no}")
def update_details(roll_no: int,student:Student):
    try:
        cur.execute(
            "UPDATE stud SET name = %s, section = %s, cgpa = %s WHERE id = %s",
            (student.name, student.section, student.cgpa, roll_no)
        )
        conn.commit()
        return {"message": "Successfully updated"}
    except Exception:
        raise HTTPException(status_code=400, detail="Couldn't update student")
@app.delete("/students/{roll_no}")
def del_stud(roll_no:int):
    try:
        cur.execute("SELECT * FROM stud WHERE id = %s", (roll_no,))
        student = cur.fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        cur.execute("DELETE FROM stud WHERE id = %s", (roll_no,))
        conn.commit()
        return {"message": "Successfully deleted"}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Couldn't delete student")
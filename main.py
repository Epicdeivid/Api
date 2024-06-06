from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Definicion de los modelos
class Content(BaseModel):
    name: str
    description: str

class Subject(BaseModel):
    name: str
    level: int
    credit_units: int
    price: float
    description: str
    contents: List[Content]

class Student(BaseModel):
    first_name: str
    last_name: str
    birth_year: int
    phone: str
    address: str
    academic_record: List[Subject]

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_year: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    academic_record: Optional[List[Subject]] = None

app = FastAPI()

# Base de datos en memoria
students_db = []

# Rutas

@app.post("/students/", response_model=Student)
def create_student(student: Student):
    students_db.append(student)
    return student

@app.get("/students/", response_model=List[Student])
def get_students():
    return students_db

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    if student_id < 0 or student_id >= len(students_db):
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]

@app.get("/students/{student_id}/academic_record", response_model=List[Subject])
def get_academic_record(student_id: int):
    if student_id < 0 or student_id >= len(students_db):
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id].academic_record

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student_update: StudentUpdate):
    if student_id < 0 or student_id >= len(students_db):
        raise HTTPException(status_code=404, detail="Student not found")

    stored_student_data = students_db[student_id].dict()
    update_data = student_update.dict(exclude_unset=True)
    updated_student = Student(**{**stored_student_data, **update_data})
    students_db[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}", response_model=Student)
def delete_student(student_id: int):
    if student_id < 0 or student_id >= len(students_db):
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db.pop(student_id)

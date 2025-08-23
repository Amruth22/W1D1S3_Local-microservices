from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Optional
import uvicorn

app = FastAPI(title="Student Personal Information Service")

# In-memory storage for student personal data
# In a real application, this would be a database
student_personal_data: Dict[str, "StudentPersonal"] = {}

class StudentPersonal(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Student Personal Information Service"}

@app.post("/students", response_model=StudentPersonal, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentPersonal):
    if student.student_id in student_personal_data:
        raise HTTPException(status_code=400, detail="Student already exists")
    student_personal_data[student.student_id] = student
    return student

@app.get("/students/{student_id}", response_model=StudentPersonal)
def read_student(student_id: str):
    if student_id not in student_personal_data:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_personal_data[student_id]

@app.put("/students/{student_id}", response_model=StudentPersonal)
def update_student(student_id: str, student_update: StudentPersonal):
    if student_id not in student_personal_data:
        raise HTTPException(status_code=404, detail="Student not found")
    student_personal_data[student_id] = student_update
    return student_update

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str):
    if student_id not in student_personal_data:
        raise HTTPException(status_code=404, detail="Student not found")
    del student_personal_data[student_id]
    return

@app.get("/students")
def list_students():
    return student_personal_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List, Optional
import requests
import uvicorn

app = FastAPI(title="Student Academic Information Service")

# In-memory storage for student academic data
# In a real application, this would be a database
student_academic_data: Dict[str, "StudentAcademic"] = {}

# Service 1 URL
SERVICE1_URL = "http://localhost:8080"

class StudentAcademic(BaseModel):
    student_id: str
    courses: List[str]
    grades: Dict[str, float]  # course: grade
    enrollment_status: str

class StudentPersonal(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class StudentCompleteInfo(BaseModel):
    personal_info: StudentPersonal
    academic_info: Optional[StudentAcademic] = None

def verify_student_exists(student_id: str) -> bool:
    """Verify if a student exists in the personal information service."""
    try:
        response = requests.get(f"{SERVICE1_URL}/students/{student_id}", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        # If service1 is down or unreachable, we might want to handle this differently
        # For now, we'll assume student doesn't exist if we can't verify
        return False

def get_student_personal_info(student_id: str) -> StudentPersonal:
    """Get student personal information from service1."""
    try:
        response = requests.get(f"{SERVICE1_URL}/students/{student_id}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return StudentPersonal(**data)
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve student personal information")
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Unable to connect to personal information service")

@app.get("/")
def read_root():
    return {"message": "Student Academic Information Service"}

@app.post("/students/{student_id}/academic", response_model=StudentAcademic, status_code=status.HTTP_201_CREATED)
def create_academic_record(student_id: str, academic_record: StudentAcademic):
    # Verify student exists in service1
    if not verify_student_exists(student_id):
        raise HTTPException(status_code=404, detail="Student not found in personal information service")
    
    # Check if academic record already exists
    if student_id in student_academic_data:
        raise HTTPException(status_code=400, detail="Academic record already exists for this student")
    
    student_academic_data[student_id] = academic_record
    return academic_record

@app.get("/students/{student_id}/academic", response_model=StudentAcademic)
def read_academic_record(student_id: str):
    if student_id not in student_academic_data:
        raise HTTPException(status_code=404, detail="Academic record not found")
    return student_academic_data[student_id]

@app.put("/students/{student_id}/academic", response_model=StudentAcademic)
def update_academic_record(student_id: str, academic_update: StudentAcademic):
    # Verify student exists in service1
    if not verify_student_exists(student_id):
        raise HTTPException(status_code=404, detail="Student not found in personal information service")
    
    if student_id not in student_academic_data:
        raise HTTPException(status_code=404, detail="Academic record not found")
    
    student_academic_data[student_id] = academic_update
    return academic_update

@app.delete("/students/{student_id}/academic", status_code=status.HTTP_204_NO_CONTENT)
def delete_academic_record(student_id: str):
    if student_id not in student_academic_data:
        raise HTTPException(status_code=404, detail="Academic record not found")
    del student_academic_data[student_id]
    return

@app.get("/students/academic")
def list_academic_records():
    return student_academic_data

@app.get("/students/{student_id}/complete", response_model=StudentCompleteInfo)
def get_complete_student_info(student_id: str):
    # Verify student exists in service1
    if not verify_student_exists(student_id):
        raise HTTPException(status_code=404, detail="Student not found in personal information service")
    
    # Get personal information from service1
    personal_info = get_student_personal_info(student_id)
    
    # Get academic information from service2 (if exists)
    academic_info = student_academic_data.get(student_id)
    
    # Return combined information
    return StudentCompleteInfo(
        personal_info=personal_info,
        academic_info=academic_info
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
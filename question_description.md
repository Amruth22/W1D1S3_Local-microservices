# Student Information Management System - Microservices Project

## Project Overview

Design and implement a local microservices architecture using FastAPI to manage student information. The system should be divided into two separate services that communicate with each other, each responsible for a specific aspect of student data.

## Requirements

### Service Structure
- Create two separate FastAPI microservices
- Each service should run on its own port (8080 and 8081)
- Both services should bind to `0.0.0.0` to be accessible on all network interfaces
- Services should communicate with each other via HTTP requests

### Service 1: Student Personal Information Service
- **Port**: 8080
- **Responsibility**: Manage student personal information
- **Data Model**: StudentPersonal
  - `student_id: str` - Unique identifier for the student
  - `first_name: str` - Student's first name
  - `last_name: str` - Student's last name
  - `email: str` - Student's email address
  - `phone: Optional[str]` - Student's phone number (optional)
  - `address: Optional[str]` - Student's address (optional)
- **Endpoints**:
  - `GET /` - Root endpoint returning service information
  - `POST /students` - Create a new student record
  - `GET /students/{student_id}` - Retrieve a specific student by ID
  - `PUT /students/{student_id}` - Update a specific student by ID
  - `DELETE /students/{student_id}` - Delete a specific student by ID
  - `GET /students` - List all student records
- **Functions**:
  - `read_root()` - Returns service information
  - `create_student(student: StudentPersonal)` - Creates a new student record
  - `read_student(student_id: str)` - Retrieves a student by ID
  - `update_student(student_id: str, student_update: StudentPersonal)` - Updates a student by ID
  - `delete_student(student_id: str)` - Deletes a student by ID
  - `list_students()` - Returns all student records

### Service 2: Student Academic Information Service
- **Port**: 8081
- **Responsibility**: Manage student academic information
- **Data Models**:
  - `StudentAcademic`:
    - `student_id: str` - Links to personal information service
    - `courses: List[str]` - List of course names
    - `grades: Dict[str, float]` - Dictionary mapping course names to grades
    - `enrollment_status: str` - Student's enrollment status
  - `StudentPersonal` (for combined endpoint):
    - `student_id: str` - Unique identifier for the student
    - `first_name: str` - Student's first name
    - `last_name: str` - Student's last name
    - `email: str` - Student's email address
    - `phone: Optional[str]` - Student's phone number (optional)
    - `address: Optional[str]` - Student's address (optional)
  - `StudentCompleteInfo` (for combined endpoint):
    - `personal_info: StudentPersonal` - Student's personal information
    - `academic_info: Optional[StudentAcademic]` - Student's academic information (optional)
- **Endpoints**:
  - `GET /` - Root endpoint returning service information
  - `POST /students/{student_id}/academic` - Create a new academic record for a student
  - `GET /students/{student_id}/academic` - Retrieve a student's academic record
  - `PUT /students/{student_id}/academic` - Update a student's academic record
  - `DELETE /students/{student_id}/academic` - Delete a student's academic record
  - `GET /students/academic` - List all academic records
  - `GET /students/{student_id}/complete` - Retrieve complete student information (personal and academic)
- **Functions**:
  - `read_root()` - Returns service information
  - `create_academic_record(student_id: str, academic_record: StudentAcademic)` - Creates a new academic record
  - `read_academic_record(student_id: str)` - Retrieves a student's academic record
  - `update_academic_record(student_id: str, academic_update: StudentAcademic)` - Updates a student's academic record
  - `delete_academic_record(student_id: str)` - Deletes a student's academic record
  - `list_academic_records()` - Returns all academic records
  - `get_complete_student_info(student_id: str)` - Returns complete student information
  - `verify_student_exists(student_id: str)` - Helper function to verify student exists in Service 1
  - `get_student_personal_info(student_id: str)` - Helper function to get student personal info from Service 1

### Inter-service Communication
- Service 2 must verify student existence in Service 1 before creating or updating academic records
- Use the `requests` library for HTTP communication between services
- Service 2 calls Service 1's `GET /students/{student_id}` endpoint for verification
- Service 2 calls Service 1's `GET /students/{student_id}` endpoint to retrieve personal information for the combined endpoint

### Additional Requirements
- Implement proper error handling with appropriate HTTP status codes:
  - 200 - Success
  - 201 - Created
  - 204 - No Content (for deletions)
  - 400 - Bad Request (e.g., duplicate records)
  - 404 - Not Found (e.g., student or record not found)
  - 503 - Service Unavailable (e.g., unable to connect to other service)
- Create unit tests to verify all functionality including error cases
- Document the services and their endpoints
- Provide a way to retrieve complete student information (both personal and academic) in a single request

### Technical Specifications
- Use FastAPI as the web framework
- Use Uvicorn as the ASGI server
- Use the `requests` library for inter-service communication
- Store data in-memory (no persistent database required)
- Follow REST API best practices
- Use Pydantic models for data validation
- Use type hints for all function parameters and return values

### Deliverables
1. Two FastAPI service files (`service1.py` and `service2.py`)
2. Requirements file (`requirements.txt`) listing all dependencies
3. Unit tests (`unit_test.py`) covering all functionality
4. Documentation (`README.md`) explaining how to run and use the services
5. This question description file (`question_description.md`)

## Expected Learning Outcomes
- Understanding of microservices architecture principles
- Implementation of inter-service communication
- REST API design and implementation
- Error handling in web services
- Unit testing for API endpoints
- Documentation best practices for software projects
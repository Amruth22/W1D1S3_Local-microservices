# Local Microservices with FastAPI

This project demonstrates a local microservices architecture using FastAPI. It consists of two services for managing student information, running on different ports and communicating via HTTP requests.

## Services

- **Service 1** (`service1.py`): Runs on `http://0.0.0.0:8080`. Manages student personal information.
- **Service 2** (`service2.py`): Runs on `http://0.0.0.0:8081`. Manages student academic information and verifies student existence with Service 1.

## Prerequisites

- Python 3.7+
- `pip` (Python package installer)

## Setup

1.  Clone or download this project.
2.  Open a terminal in the project directory.
3.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```
4.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Services

You need to run each service in a separate terminal.

### Terminal 1: Start Service 1
```bash
python service1.py
```
Service 1 will start and listen on `http://0.0.0.0:8080`.

### Terminal 2: Start Service 2
```bash
python service2.py
```
Service 2 will start and listen on `http://0.0.0.0:8081`.

## Accessing the Services and Swagger UI

Once both services are running, you can interact with them directly or through their Swagger UI.

### Service 1 Endpoints (Personal Information)

- **Root**: `http://localhost:8080/` (GET)
- **Create Student**: `http://localhost:8080/students` (POST)
- **Get Student**: `http://localhost:8080/students/{student_id}` (GET)
- **Update Student**: `http://localhost:8080/students/{student_id}` (PUT)
- **Delete Student**: `http://localhost:8080/students/{student_id}` (DELETE)
- **List All Students**: `http://localhost:8080/students` (GET)
- **Swagger UI**: `http://localhost:8080/docs`

### Service 2 Endpoints (Academic Information)

- **Root**: `http://localhost:8081/` (GET)
- **Create Academic Record**: `http://localhost:8081/students/{student_id}/academic` (POST)
- **Get Academic Record**: `http://localhost:8081/students/{student_id}/academic` (GET)
- **Update Academic Record**: `http://localhost:8081/students/{student_id}/academic` (PUT)
- **Delete Academic Record**: `http://localhost:8081/students/{student_id}/academic` (DELETE)
- **List All Academic Records**: `http://localhost:8081/students/academic` (GET)
- **Get Complete Student Info**: `http://localhost:8081/students/{student_id}/complete` (GET)
- **Swagger UI**: `http://localhost:8081/docs`

## How It Works

- `service1.py`:
  - Manages an in-memory database of student personal information.
  - Provides full CRUD operations for student personal records.
- `service2.py`:
  - Manages an in-memory database of student academic information.
  - Before creating or updating academic records, it verifies the student's existence by calling Service 1's GET endpoint.
  - Provides full CRUD operations for student academic records.
  - Provides an endpoint to retrieve complete student information (personal and academic) by combining data from both services.
- Both services use Uvicorn as the ASGI server and are configured to bind to `0.0.0.0`, making them accessible on all network interfaces of the host machine.
- Communication between services is done using the `requests` library for standard HTTP calls.
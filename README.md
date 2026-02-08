# Student Course Enrollment Service

A small REST API for managing students, courses, and enrollments. Built with **Python**, **FastAPI**, **PostgreSQL**, and **SQLAlchemy** (sync).

## Setup

1. **Clone the repository** (if not already done).

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database configuration:**
   - Ensure PostgreSQL is running and a database exists (e.g. `student_enrollment_db` on port `5433`).
   - Copy `.env.example` to `.env` and set `DATABASE_URL` if needed:
     ```bash
     copy .env.example .env
     ```
   - Default URL used by the app: `postgresql://postgres:admin123@localhost:5433/student_enrollment_db`

## How to Run

Start the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API base: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

## Example cURL Commands

Base URL: `http://localhost:8000`

### Students

```bash
# Create a student
curl -X POST "http://localhost:8000/create-student" -H "Content-Type: application/json" -d "{\"full_name\": \"John Doe\", \"email\": \"john@example.com\"}"

# List students (with pagination)
curl "http://localhost:8000/get-students?offset=0&limit=10"

# Get student by ID
curl "http://localhost:8000/get-student-by-id/1"
```

### Courses

```bash
# Create a course
curl -X POST "http://localhost:8000/create-course" -H "Content-Type: application/json" -d "{\"title\": \"Introduction to CS\", \"code\": \"CS101\", \"capacity\": 30}"

# List courses (with pagination)
curl "http://localhost:8000/get-courses?offset=0&limit=10"

# Get course by ID
curl "http://localhost:8000/get-course-by-id/1"
```

### Enrollments

```bash
# Enroll a student in a course
curl -X POST "http://localhost:8000/enrollment-student" -H "Content-Type: application/json" -d "{\"student_id\": 1, \"course_id\": 2}"

# List enrollments (optional filters: student_id, course_id, status)
curl "http://localhost:8000/get-enrollments"
curl "http://localhost:8000/get-enrollments?student_id=1&status=active"

# Cancel an enrollment
curl -X PATCH "http://localhost:8000/cancel-enrollment/1"
```

## API Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create-student` | Create student (201) |
| GET | `/get-students` | List students (offset, limit) |
| GET | `/get-student-by-id/{id}` | Get student by ID |
| POST | `/create-course` | Create course (201) |
| GET | `/get-courses` | List courses (offset, limit) |
| GET | `/get-course-by-id/{id}` | Get course by ID |
| POST | `/enrollment-student` | Enroll student (201) |
| GET | `/get-enrollments` | List enrollments (filters: student_id, course_id, status) |
| PATCH | `/cancel-enrollment/{enrollment_id}` | Cancel enrollment |

## Business Rules

- A student cannot enroll in the same course twice.
- A course cannot exceed its capacity (only **active** enrollments count).
- Cancelled enrollments do not count toward capacity.

## Error Responses

- **400** – Validation or business rule errors (e.g. "Course capacity reached", "Student already enrolled in this course", duplicate email/code).
- **404** – Resource not found (e.g. "Student not found", "Course not found", "Enrollment not found").

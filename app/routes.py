"""API Layer: FastAPI routes with business logic."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Student, Course, Enrollment, EnrollmentStatus
from app.schemas import (
    StudentCreate,
    StudentResponse,
    CourseCreate,
    CourseResponse,
    EnrollmentCreate,
    EnrollmentResponse,
)

router = APIRouter()


# ----- Students -----
@router.post("/create-student", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student. Returns 400 if email already exists."""
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student with this email already exists",
        )
    db_student = Student(full_name=student.full_name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("/get-students", response_model=list[StudentResponse])
def get_students(
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """List students with pagination."""
    return db.query(Student).offset(offset).limit(limit).all()


@router.get("/get-student-by-id/{id}", response_model=StudentResponse)
def get_student_by_id(id: int, db: Session = Depends(get_db)):
    """Get a single student by ID."""
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ----- Courses -----
@router.post("/create-course", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course. Returns 400 if course code already exists."""
    existing = db.query(Course).filter(Course.code == course.code).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Course with this code already exists",
        )
    db_course = Course(
        title=course.title,
        code=course.code,
        capacity=course.capacity,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/get-courses", response_model=list[CourseResponse])
def get_courses(
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """List courses with pagination."""
    return db.query(Course).offset(offset).limit(limit).all()


@router.get("/get-course-by-id/{id}", response_model=CourseResponse)
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    """Get a single course by ID."""
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# ----- Enrollments -----
@router.post("/enrollment-student", response_model=EnrollmentResponse, status_code=201)
def enrollment_student(body: EnrollmentCreate, db: Session = Depends(get_db)):
    """
    Enroll a student in a course.
    Enforces: student/course exist, no duplicate enrollment, course capacity.
    """
    student = db.query(Student).filter(Student.id == body.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    course = db.query(Course).filter(Course.id == body.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == body.student_id,
            Enrollment.course_id == body.course_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student already enrolled in this course",
        )

    active_count = (
        db.query(func.count(Enrollment.id))
        .filter(
            Enrollment.course_id == body.course_id,
            Enrollment.status == EnrollmentStatus.active,
        )
        .scalar()
    )
    if active_count >= course.capacity:
        raise HTTPException(
            status_code=400,
            detail="Course capacity reached",
        )

    enrollment = Enrollment(
        student_id=body.student_id,
        course_id=body.course_id,
        status=EnrollmentStatus.active,
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/get-enrollments", response_model=list[EnrollmentResponse])
def get_enrollments(
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List enrollments with optional filters."""
    q = db.query(Enrollment)
    if student_id is not None:
        q = q.filter(Enrollment.student_id == student_id)
    if course_id is not None:
        q = q.filter(Enrollment.course_id == course_id)
    if status is not None:
        q = q.filter(Enrollment.status == status)
    return q.all()


@router.patch("/cancel-enrollment/{enrollment_id}", response_model=EnrollmentResponse)
def cancel_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """Cancel an enrollment by setting status to cancelled."""
    enrollment = (
        db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment.status = EnrollmentStatus.cancelled
    db.commit()
    db.refresh(enrollment)
    return enrollment

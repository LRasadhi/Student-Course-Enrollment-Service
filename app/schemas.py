"""Pydantic schemas for request and response validation."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ----- Student -----
class StudentCreate(BaseModel):
    """Request body for creating a student."""
    full_name: str
    email: EmailStr


class StudentResponse(BaseModel):
    """Response model for a student."""
    id: int
    full_name: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ----- Course -----
class CourseCreate(BaseModel):
    """Request body for creating a course."""
    title: str
    code: str
    capacity: int = Field(default=30, ge=1)


class CourseResponse(BaseModel):
    """Response model for a course."""
    id: int
    title: str
    code: str
    capacity: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ----- Enrollment -----
class EnrollmentCreate(BaseModel):
    """Request body for enrolling a student in a course."""
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    """Response model for an enrollment."""
    id: int
    student_id: int
    course_id: int
    status: str
    enrolled_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


# ----- Error -----
class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str

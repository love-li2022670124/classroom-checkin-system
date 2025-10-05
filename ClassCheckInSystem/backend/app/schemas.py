from pydantic import BaseModel, Field  # pyright: ignore[reportMissingImports]
from typing import Optional, List
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    user_id: int
    name: str
    role: str


class AttendanceCreate(BaseModel):
    course_id: int
    class_id: Optional[int] = None
    student_id: int
    status: str
    sign_method: str
    sign_time: Optional[datetime] = None
    sign_location_lng: Optional[str] = None
    sign_location_lat: Optional[str] = None
    sign_location_address: Optional[str] = None
    remark: Optional[str] = None


class AttendanceOut(BaseModel):
    record_id: int
    course_id: int
    class_id: Optional[int] = None
    student_id: int
    status: str
    sign_method: str
    sign_time: Optional[datetime]

    class Config:
        from_attributes = True


class MakeupApply(BaseModel):
    student_id: int
    course_id: int
    apply_reason: str


class AttendanceQuery(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    class_id: Optional[int] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class AttendanceRateOut(BaseModel):
    course_id: int
    present: int
    total: int
    rate: float = Field(..., description="0~1")

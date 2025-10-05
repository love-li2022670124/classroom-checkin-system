from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import relationship  # pyright: ignore[reportMissingImports]
from .database import Base
import enum


class RoleEnum(str, enum.Enum):
    admin = "ADMIN"
    teacher = "TEACHER"
    student = "STUDENT"


class UserBase(Base):
    __tablename__ = "user_base"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    name = Column(String(50), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)


class Admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    user_base_id = Column(Integer, ForeignKey("user_base.user_id"), nullable=False)
    admin_no = Column(String(20), unique=True)
    department = Column(String(50))
    permission_level = Column(String(20))


class Class(Base):
    __tablename__ = "class"
    class_id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(50), nullable=False)
    grade = Column(Integer)

    students = relationship("Student", back_populates="clazz")


class Student(Base):
    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    user_base_id = Column(Integer, ForeignKey("user_base.user_id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class.class_id"))
    grade = Column(Integer)
    major = Column(String(50))

    user = relationship("UserBase", back_populates="student")
    clazz = relationship("Class", back_populates="students")


class Teacher(Base):
    __tablename__ = "teacher"
    teacher_id = Column(Integer, primary_key=True, autoincrement=True)
    user_base_id = Column(Integer, ForeignKey("user_base.user_id"), nullable=False)
    teacher_no = Column(String(20), unique=True)
    department = Column(String(50))
    title = Column(String(20))

    user = relationship("UserBase", back_populates="teacher")


class Course(Base):
    __tablename__ = "course"
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(50), nullable=False)
    credit = Column(Integer)


class CourseTeach(Base):
    __tablename__ = "course_teach"
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("course.course_id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id"), nullable=False)


class ClassCourse(Base):
    __tablename__ = "class_course"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey("class.class_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.course_id"), nullable=False)


class RecordStatus(str, enum.Enum):
    present = "Present"
    absent = "Absent"
    late = "Late"
    leave = "Leave"


class SignMethod(str, enum.Enum):
    qrcode = "QRCode"
    location = "Location"
    makeup = "Makeup"


class AttendanceRecord(Base):
    __tablename__ = "attendance_record"
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("course.course_id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class.class_id"))
    student_id = Column(Integer, ForeignKey("student.student_id"), nullable=False)
    sign_time = Column(DateTime)
    sign_type = Column(String(20))
    sign_method = Column(Enum(SignMethod))
    sign_location_lng = Column(String(20))
    sign_location_lat = Column(String(20))
    sign_location_address = Column(String(255))
    status = Column(Enum(RecordStatus), nullable=False)
    remark = Column(String(255))


class MakeupStatus(str, enum.Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"


class MakeUpRecord(Base):
    __tablename__ = "make_up_record"
    make_up_id = Column(Integer, primary_key=True, autoincrement=True)
    attendance_record_id = Column(Integer, ForeignKey("attendance_record.record_id"))
    operator_type = Column(String(20))
    operator_id = Column(Integer)
    apply_reason = Column(String(255))
    approve_reason = Column(String(255))
    status = Column(Enum(MakeupStatus), default=MakeupStatus.pending)
    create_time = Column(DateTime)
    approve_time = Column(DateTime)


class FeedbackStatus(str, enum.Enum):
    open = "Open"
    resolved = "Resolved"


class Feedback(Base):
    __tablename__ = "feedback"
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("attendance_record.record_id"))
    student_id = Column(Integer, ForeignKey("student.student_id"))
    feedback_content = Column(Text)
    create_time = Column(DateTime)
    status = Column(Enum(FeedbackStatus), default=FeedbackStatus.open)
    handle_remark = Column(Text)
    handle_time = Column(DateTime)

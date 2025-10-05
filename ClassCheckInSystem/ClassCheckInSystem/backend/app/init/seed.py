from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from sqlalchemy import text  # pyright: ignore[reportMissingImports]
from ..database import SessionLocal, engine, Base
from ..models import UserBase, RoleEnum, Class, Student, Teacher, Course
from ..auth import get_password_hash


def upsert_user(db: Session, username: str, name: str, role: RoleEnum, password: str) -> UserBase:
    user = db.query(UserBase).filter(UserBase.username == username).first()
    if user:
        return user
    user = UserBase(username=username, name=name, role=role, password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # users
        admin = upsert_user(db, "admin", "管理员", RoleEnum.admin, "admin123")
        t1 = upsert_user(db, "t001", "张老师", RoleEnum.teacher, "pass123")
        s1 = upsert_user(db, "s001", "小明", RoleEnum.student, "pass123")
        s2 = upsert_user(db, "s002", "小红", RoleEnum.student, "pass123")

        # class
        clazz = db.query(Class).first()
        if not clazz:
            clazz = Class(class_name="计科2201", grade=2022)
            db.add(clazz)
            db.commit()
            db.refresh(clazz)

        # student
        if not db.query(Student).first():
            st1 = Student(user_base_id=s1.user_id, class_id=clazz.class_id, grade=2022, major="计算机科学")
            st2 = Student(user_base_id=s2.user_id, class_id=clazz.class_id, grade=2022, major="计算机科学")
            db.add_all([st1, st2])
            db.commit()

        # teacher
        if not db.query(Teacher).first():
            teacher = Teacher(user_base_id=t1.user_id, teacher_no="T001", department="计算机学院", title="讲师")
            db.add(teacher)
            db.commit()

        # courses
        if not db.query(Course).first():
            db.add_all([
                Course(course_name="数据结构", credit=3),
                Course(course_name="操作系统", credit=3),
            ])
            db.commit()

        print("Seed data inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    run()

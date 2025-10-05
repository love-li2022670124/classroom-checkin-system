from fastapi import APIRouter, Depends  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
import pandas as pd  # pyright: ignore[reportMissingImports]
from io import BytesIO
from fastapi.responses import StreamingResponse  # pyright: ignore[reportMissingImports]
from sqlalchemy import func  # pyright: ignore[reportMissingImports]
from datetime import datetime
from .database import get_db  # pyright: ignore[reportMissingImports]
from .models import UserBase, Course, AttendanceRecord, RecordStatus, RoleEnum  # pyright: ignore[reportMissingImports]
from .deps.roles import require_roles  # pyright: ignore[reportMissingImports]

router = APIRouter(prefix="/admin", tags=["admin"])

admin_only = Depends(require_roles(RoleEnum.admin))


@router.get("/users")
def list_users(db: Session = Depends(get_db), _=admin_only):
    users = db.query(UserBase).limit(200).all()
    return [{"user_id": u.user_id, "username": u.username, "name": u.name, "role": u.role.value} for u in users]


@router.post("/course")
def create_course(course_name: str, credit: int = 0, db: Session = Depends(get_db), _=admin_only):
    c = Course(course_name=course_name, credit=credit)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"course_id": c.course_id}


@router.get("/report/export")
def export_report(start: str, end: str, db: Session = Depends(get_db), _=admin_only):
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    recs = db.query(AttendanceRecord).filter(AttendanceRecord.sign_time >= start_dt, AttendanceRecord.sign_time <= end_dt).all()
    rows = [{
        "record_id": r.record_id,
        "course_id": r.course_id,
        "student_id": r.student_id,
        "status": r.status.value if hasattr(r.status, 'value') else str(r.status),
        "sign_method": r.sign_method.value if hasattr(r.sign_method, 'value') else str(r.sign_method),
        "sign_time": r.sign_time,
    } for r in recs]
    df = pd.DataFrame(rows)
    buf = BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=attendance.xlsx"})


@router.get("/statistics/trend")
def statistics_trend(start: str, end: str, db: Session = Depends(get_db), _=admin_only):
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    rows = (
        db.query(func.date(AttendanceRecord.sign_time), func.count(AttendanceRecord.record_id))
        .filter(AttendanceRecord.sign_time >= start_dt, AttendanceRecord.sign_time <= end_dt, AttendanceRecord.status == RecordStatus.present)
        .group_by(func.date(AttendanceRecord.sign_time))
        .all()
    )
    return [{"date": str(d), "count": int(c)} for d, c in rows]

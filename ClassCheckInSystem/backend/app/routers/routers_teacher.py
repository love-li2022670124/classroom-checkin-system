from fastapi import APIRouter, Depends, HTTPException  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from sqlalchemy import func  # pyright: ignore[reportMissingImports]
from datetime import datetime
from .database import get_db  # pyright: ignore[reportMissingImports]
from .models import AttendanceRecord, RecordStatus, SignMethod, MakeUpRecord, MakeupStatus, UserBase, RoleEnum  # pyright: ignore[reportMissingImports]
from .schemas import AttendanceQuery, AttendanceRateOut  # pyright: ignore[reportMissingImports]
from .deps.roles import require_roles  # pyright: ignore[reportMissingImports]

router = APIRouter(prefix="/teacher", tags=["teacher"])

teacher_only = Depends(require_roles(RoleEnum.teacher, RoleEnum.admin))


@router.get("/attendance/rate", response_model=list[AttendanceRateOut])
def attendance_rate(course_id: int, db: Session = Depends(get_db), _=teacher_only):
    total = db.query(func.count(AttendanceRecord.record_id)).filter(AttendanceRecord.course_id == course_id).scalar() or 0
    present = db.query(func.count(AttendanceRecord.record_id)).filter(AttendanceRecord.course_id == course_id, AttendanceRecord.status == RecordStatus.present).scalar() or 0
    rate = 0.0 if total == 0 else present / total
    return [AttendanceRateOut(course_id=course_id, present=present, total=total, rate=rate)]


@router.post("/sign/makeup")
def manual_makeup(student_id: int, course_id: int, reason: str, db: Session = Depends(get_db), _=teacher_only):
    makeup = MakeUpRecord(
        operator_type="Teacher",
        operator_id=0,
        apply_reason=reason,
        status=MakeupStatus.approved,
        create_time=datetime.utcnow(),
        approve_time=datetime.utcnow(),
    )
    db.add(makeup)
    db.flush()
    record = AttendanceRecord(
        course_id=course_id,
        student_id=student_id,
        sign_time=datetime.utcnow(),
        sign_method=SignMethod.makeup,
        status=RecordStatus.present,
        remark=f"makeup_id={makeup.make_up_id}",
    )
    db.add(record)
    db.commit()
    return {"make_up_id": makeup.make_up_id}


@router.post("/record/query")
def query_records(q: AttendanceQuery, db: Session = Depends(get_db), _=teacher_only):
    query = db.query(AttendanceRecord)
    if q.student_id:
        query = query.filter(AttendanceRecord.student_id == q.student_id)
    if q.course_id:
        query = query.filter(AttendanceRecord.course_id == q.course_id)
    if q.class_id:
        query = query.filter(AttendanceRecord.class_id == q.class_id)
    if q.start:
        query = query.filter(AttendanceRecord.sign_time >= q.start)
    if q.end:
        query = query.filter(AttendanceRecord.sign_time <= q.end)
    return [{
        "record_id": r.record_id,
        "course_id": r.course_id,
        "student_id": r.student_id,
        "status": r.status.value if hasattr(r.status, 'value') else str(r.status),
        "sign_method": r.sign_method.value if hasattr(r.sign_method, 'value') else str(r.sign_method),
        "sign_time": r.sign_time.isoformat() if r.sign_time else None,
    } for r in query.order_by(AttendanceRecord.record_id.desc()).limit(500).all()]

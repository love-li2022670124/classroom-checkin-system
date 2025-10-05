from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from datetime import datetime
from ..models import AttendanceRecord, RecordStatus, SignMethod


def create_record(db: Session, *, course_id: int, student_id: int, status: RecordStatus, method: SignMethod, remark: str | None = None, lng: str | None = None, lat: str | None = None) -> AttendanceRecord:
    rec = AttendanceRecord(
        course_id=course_id,
        student_id=student_id,
        sign_time=datetime.utcnow(),
        status=status,
        sign_method=method,
        remark=remark,
        sign_location_lng=lng,
        sign_location_lat=lat,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

from fastapi import APIRouter, Depends, HTTPException  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from geopy.distance import geodesic  # pyright: ignore[reportMissingImports]
from ..database import get_db
from ..models import AttendanceRecord, RecordStatus, SignMethod, UserBase, RoleEnum
from ..schemas import AttendanceOut
from ..deps.roles import require_roles
from ..services.qrcode_service import generate_qr_token, consume_qr_token
from ..crud.attendance import create_record

router = APIRouter(prefix="/student", tags=["student"])

student_only = require_roles(RoleEnum.student, RoleEnum.teacher, RoleEnum.admin)


@router.post("/sign/qrcode/create")
def create_qr_token(course_id: int, user: UserBase = Depends(require_roles(RoleEnum.teacher, RoleEnum.admin))):
    token = generate_qr_token(course_id)
    return {"qr_token": token}


@router.post("/sign/qrcode/verify")
def sign_by_qrcode(qr_token: str, course_id: int, student_id: int, db: Session = Depends(get_db), user: UserBase = Depends(student_only)):
    if not consume_qr_token(qr_token):
        raise HTTPException(status_code=400, detail="二维码无效或过期")
    record = create_record(db, course_id=course_id, student_id=student_id, status=RecordStatus.present, method=SignMethod.qrcode)
    return {"record_id": record.record_id}


@router.post("/sign/location")
def sign_by_location(course_id: int, student_id: int, lng: float, lat: float, room_lng: float, room_lat: float, db: Session = Depends(get_db), user: UserBase = Depends(student_only)):
    distance_m = geodesic((lat, lng), (room_lat, room_lng)).meters
    if distance_m > 1000:
        raise HTTPException(status_code=400, detail="位置超出范围，请到教室附近签到")
    record = create_record(db, course_id=course_id, student_id=student_id, status=RecordStatus.present, method=SignMethod.location, lng=str(lng), lat=str(lat))
    return {"record_id": record.record_id, "distance_m": round(distance_m, 2)}


@router.get("/record/personal", response_model=list[AttendanceOut])
def personal_records(student_id: int, db: Session = Depends(get_db), user: UserBase = Depends(student_only)):
    recs = (
        db.query(AttendanceRecord)
        .filter(AttendanceRecord.student_id == student_id)
        .order_by(AttendanceRecord.record_id.desc())
        .limit(200)
        .all()
    )
    return recs

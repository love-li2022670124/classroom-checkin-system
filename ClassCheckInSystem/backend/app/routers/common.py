from fastapi import APIRouter, Depends, HTTPException  # pyright: ignore[reportMissingImports]
from fastapi.security import OAuth2PasswordRequestForm  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
from ..database import get_db
from ..models import UserBase
from ..auth import verify_password, create_access_token

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserBase).filter(UserBase.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    token = create_access_token({"sub": user.username, "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}

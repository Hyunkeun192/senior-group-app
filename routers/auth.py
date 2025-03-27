from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.models import User, Provider  # ✅ Provider 모델도 import
from database import SessionLocal
from routers.auth_utils import get_current_user, create_access_token
from passlib.context import CryptContext
from schemas import TokenResponse, UserResponse  # ✅ 직접 import
import crud

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 비밀번호 해싱 함수
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 사용자 로그인 (JWT 발급)
@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="이메일이 존재하지 않습니다.")
    
    if not user.password_hash or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="비밀번호가 틀렸거나 해싱되지 않은 값입니다.")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ 현재 로그인한 사용자 정보
@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# ✅ 업체 로그인용 API
@router.post("/provider-login", response_model=TokenResponse)
def provider_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    provider = crud.get_provider_by_email(db, form_data.username)
    if not provider:
        raise HTTPException(status_code=400, detail="해당 이메일의 업체가 없습니다.")

    if not provider.password_hash or not pwd_context.verify(form_data.password, provider.password_hash):
        raise HTTPException(status_code=400, detail="비밀번호가 틀렸거나 해싱되지 않은 값입니다.")

    access_token = create_access_token(data={"sub": provider.email})
    return {"access_token": access_token, "token_type": "bearer"}

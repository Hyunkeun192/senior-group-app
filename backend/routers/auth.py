from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.models import User, Provider, Admin
from database import get_db  # ✅ get_db 가져오기
from auth_utils import get_current_user, create_access_token, create_admin_access_token, verify_password
from passlib.context import CryptContext
from schemas import TokenResponse, UserResponse
from datetime import datetime, timedelta

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 사용자 로그인 (JWT 발급)
@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="이메일이 존재하지 않습니다.")
    if not user.password_hash or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ 현재 로그인한 사용자 정보
@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# ✅ 업체 로그인용 API
@router.post("/provider-login", response_model=TokenResponse)
def provider_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.email == form_data.username).first()
    if not provider:
        raise HTTPException(status_code=400, detail="업체를 찾을 수 없습니다.")
    if not verify_password(form_data.password, provider.password_hash):
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")

    access_token = create_access_token(data={"sub": provider.id})
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ 관리자 인증 함수
def get_current_admin(request: Request, db: Session = Depends(get_db)) -> Admin:
    token = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="관리자 인증 정보가 없습니다.")

    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        admin_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="잘못된 관리자 토큰입니다.")

    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=401, detail="관리자 계정을 찾을 수 없습니다.")

    return admin

__all__ = ["router"]

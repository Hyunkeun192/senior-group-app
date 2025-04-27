from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models.models import Admin
from schemas import AdminLoginRequest, AdminSignupRequest, TokenResponse
from auth_utils import create_admin_access_token

router = APIRouter(prefix="/admin", tags=["Admin Login"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 관리자 로그인
@router.post("/login", response_model=TokenResponse)
def admin_login(login_req: AdminLoginRequest = Body(...), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == login_req.email).first()
    if not admin:
        raise HTTPException(status_code=401, detail="이메일이 존재하지 않습니다.")
    if not pwd_context.verify(login_req.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

    token = create_admin_access_token({"sub": str(admin.id)})
    return {"access_token": token, "token_type": "bearer"}

# ✅ 관리자 회원가입
@router.post("/signup")
def admin_signup(request: AdminSignupRequest, db: Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter(Admin.email == request.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    new_admin = Admin(
        email=request.email,
        password_hash=pwd_context.hash(request.password)
    )
    db.add(new_admin)
    db.commit()
    return {"message": "관리자 계정이 생성되었습니다."}

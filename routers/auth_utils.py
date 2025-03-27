from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import User

# 🔑 환경 변수 로딩
load_dotenv()

# 🔐 JWT 설정값
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# ✅ 토큰 발급 함수 (🔥 sub 포함 필수)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "sub": data.get("sub")  # ✅ 꼭 필요!
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ✅ OAuth2PasswordBearer: 토큰 추출 정의
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ✅ DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 현재 로그인한 사용자 정보 추출
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("🪪 받은 토큰:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print("📧 JWT payload sub:", email)
        if email is None:
            raise HTTPException(status_code=401, detail="토큰에 사용자 정보 없음")
    except JWTError as e:
        print("❌ JWT 디코딩 오류:", str(e))
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        print("❌ 사용자 찾을 수 없음:", email)
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다")

    print("✅ 인증된 사용자:", user.email)
    return user

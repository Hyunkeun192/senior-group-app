import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
from models.models import User, Provider, Admin

# ✅ .env 파일 로딩
load_dotenv()

# ✅ 환경 변수 설정
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

# ✅ 비밀번호 해시 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 사용자용 토큰 스키마
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ✅ 업체용 토큰 스키마
oauth2_scheme_provider = OAuth2PasswordBearer(tokenUrl="/providers/login")

# ✅ 관리자용 토큰 스키마
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="/admin/login")

# ✅ 비밀번호 해시 함수
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ 사용자용 토큰 발급
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# ✅ 관리자용 토큰 발급
def create_admin_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# ✅ 현재 사용자 추출
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="토큰에 사용자 정보 없음")
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다")

    return user

# ✅ 현재 업체 추출
def get_current_provider(token: str = Depends(oauth2_scheme_provider), db: Session = Depends(get_db)) -> Provider:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="업체 인증 정보가 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        print("💡 decoded email from token:", email)  # ✅ 디버깅 로그 추가
        if email is None:
            raise credentials_exception
    except JWTError as e:
        print("❌ JWT Error:", str(e))  # ✅ 디버깅 로그 추가
        raise credentials_exception

    provider_id = int(payload.get("sub"))  # 숫자 ID로 받아오고
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    print("🔍 provider found:", provider)  # ✅ 디버깅 로그 추가

    if provider is None:
        raise credentials_exception

    return provider


# ✅ 현재 관리자 추출
def get_current_admin(token: str = Depends(oauth2_scheme_admin), db: Session = Depends(get_db)) -> Admin:
    print("🔐 get_current_admin called!")  # ✅ 함수 호출 로그

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="관리자 인증 정보가 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        print(f"👉 decoded payload: {payload}")  # ✅ payload 로그

        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception

        admin_id = int(sub)
        print(f"👉 parsed admin_id: {admin_id}")  # ✅ admin_id 로그
    except (JWTError, ValueError) as e:
        print(f"❌ Token decoding or conversion error: {e}")  # ✅ 예외 로그
        raise credentials_exception

    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if admin is None:
        print("❌ Admin not found in DB!")  # ✅ 관리자 미존재 로그
        raise credentials_exception

    print(f"✅ Admin found: {admin.email}")  # ✅ 관리자 존재 확인 로그
    return admin



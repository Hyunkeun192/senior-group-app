from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app import crud
from app import models, schemas

router = APIRouter()

# 사용자 회원가입 API
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 중복 이메일 체크
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 새 사용자 생성
    return crud.create_user(db, user)

# 특정 사용자 조회 API (이메일 기준)
@router.get("/{email}", response_model=UserResponse)
def get_user(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 전체 사용자 조회 API
@router.get("/", response_model=list[UserResponse])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

# 모든 업체 조회
def get_providers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Provider).offset(skip).limit(limit).all()

# 특정 업체 조회
def get_provider_by_id(db: Session, provider_id: int):
    return db.query(models.Provider).filter(models.Provider.id == provider_id).first()

# 신규 업체 등록
def create_provider(db: Session, provider: schemas.ProviderResponse):
    db_provider = models.Provider(
        name=provider.name,
        email=provider.email,
        phone=provider.phone,
        service_area=provider.service_area,
        services=provider.services
    )
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

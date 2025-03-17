from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# 데이터베이스 세션 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 모든 사용자 조회
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# 특정 사용자 조회
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from database import get_db  # ✅ get_db 직접 import
from auth_utils import get_current_user  # ✅ 로그인 유저 의존성 주입
from schemas import UserCreate, UserResponse, UserUpdate, CustomInterestCreate  # ✅ schemas import
from models.models import CustomInterest

router = APIRouter()

# ✅ 사용자 회원가입 API (중복 이메일 방지)
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    return crud.create_user(db, user)

# ✅ 현재 로그인한 사용자 정보 조회 API
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user

# ✅ 사용자 ID로 조회 API
@router.get("/users/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return db_user

# ✅ 사용자 정보 수정 API
@router.put("/users/me", response_model=UserResponse)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated_user = crud.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return updated_user

# ✅ 사용자 삭제 API
@router.delete("/users/me", response_model=UserResponse)
def delete_user_me(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted_user = crud.delete_user(db, current_user.id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return deleted_user

# ✅ 사용자 주관식 관심사 등록 API
@router.post("/custom-interests")
def create_custom_interest(
    interest: CustomInterestCreate,
    db: Session = Depends(get_db)
):
    new_interest = CustomInterest(
        value=interest.value  # ⛳ user_id 제거 (nullable=True로 가정)
    )
    db.add(new_interest)
    db.commit()
    db.refresh(new_interest)
    return new_interest

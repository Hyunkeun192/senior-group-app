from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import crud
from schemas import (
    ProviderCreate, ProviderUpdate, ProviderResponse,
    ActivityParticipantsResponse, ActivityResponse
)
from auth_utils import get_current_provider, create_access_token, verify_password
from database import get_db
from models.models import Provider
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 로그인한 provider 본인 정보 확인 API
@router.get("/providers/me", response_model=ProviderResponse)
def read_current_provider(current_provider: Provider = Depends(get_current_provider)):
    return current_provider

# ✅ 로그인한 provider의 활동 목록 조회
@router.get("/providers/my-activities", response_model=list[ActivityResponse])
def get_my_activities(current_provider: Provider = Depends(get_current_provider), db: Session = Depends(get_db)):
    return crud.get_activities_by_provider(db, current_provider.id)

# ✅ 특정 provider의 활동 목록 조회
@router.get("/providers/{provider_id}/activities", response_model=list[ActivityResponse])
def get_activities_by_provider(provider_id: int, db: Session = Depends(get_db)):
    return crud.get_activities_by_provider(db, provider_id)

# ✅ 업체 등록
@router.post("/providers/", response_model=ProviderResponse)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(provider.password)
    db_provider = Provider(
        name=provider.name,
        email=provider.email,
        service_name=provider.service_name,
        phone=provider.phone,
        password_hash=hashed_password,
        service_area=provider.service_area,
        is_business=provider.is_business,
        business_registration_number=provider.business_registration_number,
    )
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

# ✅ 업체 조회
@router.get("/providers/{provider_id}", response_model=ProviderResponse)
def read_provider_by_id(provider_id: int, db: Session = Depends(get_db)):
    db_provider = crud.get_provider_by_id(db, provider_id)
    if not db_provider:
        raise HTTPException(status_code=404, detail="업체를 찾을 수 없습니다.")
    return db_provider

# ✅ 업체 정보 수정
@router.put("/providers/{provider_id}", response_model=ProviderResponse)
def update_provider(provider_id: int, update: ProviderUpdate, db: Session = Depends(get_db)):
    updated = crud.update_provider(db, provider_id, update)
    if not updated:
        raise HTTPException(status_code=404, detail="업체를 찾을 수 없습니다.")
    return updated

# ✅ 업체 삭제
@router.delete("/providers/{provider_id}", response_model=ProviderResponse)
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_provider(db, provider_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="업체를 찾을 수 없습니다.")
    return deleted

# ✅ 활동별 현재 참여자 수 확인
@router.get("/providers/{provider_id}/activity-participants", response_model=list[ActivityParticipantsResponse])
def get_activity_participants(provider_id: int, db: Session = Depends(get_db)):
    return crud.get_activity_participants_for_provider(db, provider_id)

# ✅ 업체 로그인 API - JWT 토큰 발급
@router.post("/providers/login")
def provider_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    provider = crud.get_provider_by_email(db, form_data.username)
    if not provider:
        raise HTTPException(status_code=401, detail="존재하지 않는 이메일입니다.")
    if not verify_password(form_data.password, provider.password_hash):
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

    access_token = create_access_token(data={"sub": provider.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "provider": {
            "id": provider.id,
            "name": provider.name,
            "email": provider.email
        }
    }

# ✅ 활동 + 참여자 수 포함된 목록 API
@router.get("/providers/{provider_id}/activities/with-counts")
def get_provider_activities_with_counts_api(provider_id: int, db: Session = Depends(get_db)):
    return crud.get_provider_activities_with_counts(db, provider_id)

# ✅ 현재 로그인한 provider 삭제
@router.delete("/providers/me", response_model=dict)
def delete_current_provider(db: Session = Depends(get_db), current_provider: Provider = Depends(get_current_provider)):
    db.delete(current_provider)
    db.commit()
    return {"message": "업체 탈퇴 완료"}

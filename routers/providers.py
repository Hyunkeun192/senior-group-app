from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from schemas import ProviderCreate, ProviderUpdate, ProviderResponse, ActivityParticipantsResponse  # ✅ 직접 import로 변경

router = APIRouter()

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 업체 등록 API
@router.post("/providers/", response_model=ProviderResponse)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    return crud.create_provider(db, provider)

# ✅ 업체 조회 API
@router.get("/providers/{provider_id}", response_model=ProviderResponse)
def read_provider_by_id(provider_id: int, db: Session = Depends(get_db)):
    db_provider = crud.get_provider_by_id(db, provider_id)
    if not db_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider

# ✅ 업체 정보 수정 API
@router.put("/providers/{provider_id}", response_model=ProviderResponse)
def update_provider(provider_id: int, update: ProviderUpdate, db: Session = Depends(get_db)):
    updated = crud.update_provider(db, provider_id, update)
    if not updated:
        raise HTTPException(status_code=404, detail="Provider not found")
    return updated

# ✅ 업체 삭제 API
@router.delete("/providers/{provider_id}", response_model=ProviderResponse)
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_provider(db, provider_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Provider not found")
    return deleted

# ✅ 활동별 현재 참여자 수 확인 API (provider 대시보드용)
@router.get("/providers/{provider_id}/activity-participants", response_model=list[ActivityParticipantsResponse])
def get_activity_participants(provider_id: int, db: Session = Depends(get_db)):
    return crud.get_activity_participants_for_provider(db, provider_id)

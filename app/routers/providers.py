from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.crud import get_providers, get_provider_by_id, create_provider


router = APIRouter()  # ✅ FastAPI의 APIRouter 객체 생성

# 모든 업체 조회 API
@router.get("/", response_model=list[schemas.ProviderResponse])
def get_all_providers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_providers(db, skip=skip, limit=limit)

# 특정 업체 조회 API (ID 기준)
@router.get("/{provider_id}", response_model=schemas.ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = crud.get_provider_by_id(db, provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

# 신규 업체 등록 API
@router.post("/", response_model=schemas.ProviderResponse)
def create_provider(provider: schemas.ProviderResponse, db: Session = Depends(get_db)):
    return crud.create_provider(db, provider)

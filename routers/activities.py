from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from schemas import ActivityCreate, ActivityResponse, ActivityUpdate  # ✅ 직접 import로 수정

router = APIRouter()

# ✅ DB 세션 의존성 추가
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 활동 등록 API
@router.post("/activities/", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    return crud.create_activity(db, activity)

# ✅ 활동 전체 조회 API
@router.get("/activities/", response_model=list[ActivityResponse])
def read_activities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_activities(db, skip=skip, limit=limit)

# ✅ 활동 단건 조회 API
@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = crud.get_activity_by_id(db, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

# ✅ 활동 수정 API
@router.put("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, update: ActivityUpdate, db: Session = Depends(get_db)):
    updated = crud.update_activity(db, activity_id, update)
    if not updated:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated

# ✅ 활동 삭제 API
@router.delete("/activities/{activity_id}", response_model=ActivityResponse)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_activity(db, activity_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Activity not found")
    return deleted

# ✅ 모집 부족한 활동 조회 API
@router.get("/activities/insufficient")
def get_insufficient_activities(db: Session = Depends(get_db)):
    return crud.get_insufficient_activities(db)

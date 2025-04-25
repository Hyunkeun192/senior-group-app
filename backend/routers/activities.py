from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from schemas import ActivityCreate, ActivityResponse, ActivityUpdate, ActivityDeadlineUpdate
from models.models import Provider, Notification, Subscription
from auth_utils import get_current_provider
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/activities")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ActivityResponse)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_provider: Provider = Depends(get_current_provider)
):
    if not current_provider.is_approved:
        raise HTTPException(status_code=403, detail="승인되지 않은 업체는 활동을 등록할 수 없습니다.")
    activity.provider_id = current_provider.id
    return crud.create_activity(db, activity)

@router.get("/", response_model=list[ActivityResponse])
def read_activities(
    region: Optional[str] = None,
    interest: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_activities_with_filter(db, region, interest)

@router.get("/{activity_id}", response_model=ActivityResponse)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = crud.get_activity_by_id(db, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@router.put("/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, update: ActivityUpdate, db: Session = Depends(get_db)):
    updated = crud.update_activity(db, activity_id, update)
    if not updated:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated

@router.delete("/{activity_id}", response_model=ActivityResponse)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_activity(db, activity_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Activity not found")
    return deleted

@router.get("/insufficient")
def get_insufficient_activities(db: Session = Depends(get_db)):
    return crud.get_insufficient_activities(db)

@router.patch("/{activity_id}/confirm", response_model=ActivityResponse)
def confirm_activity(
    activity_id: int,
    current_provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db)
):
    result = crud.confirm_activity(db, activity_id, current_provider.id)

    if result is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not authorized to confirm this activity")
    if result == "already_confirmed":
        raise HTTPException(status_code=400, detail="Activity already confirmed")
    if result == "not_enough_participants":
        raise HTTPException(status_code=400, detail="Not enough participants to confirm")

    # ✅ 사용자에게 알림 전송
    subscriptions = db.query(Subscription).filter(
        Subscription.activity_id == activity_id
    ).distinct(Subscription.user_id).all()

    for sub in subscriptions:
        if sub.user_id:
            notification = Notification(
                user_id=sub.user_id,
                message="모집하신 활동이 확정되었습니다! 결제를 진행해주세요.",
                is_read=False,
                created_at=datetime.utcnow()
            )
            db.add(notification)

    db.commit()
    return result

@router.patch("/{activity_id}/cancel", response_model=ActivityResponse)
def cancel_activity(
    activity_id: int,
    current_provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db)
):
    result = crud.cancel_activity(db, activity_id, current_provider.id)

    if result is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not authorized to cancel this activity")

    return result

@router.patch("/{activity_id}/deadline", response_model=ActivityResponse)
def update_deadline(
    activity_id: int,
    deadline_data: ActivityDeadlineUpdate,
    current_provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db)
):
    result = crud.update_activity_deadline(db, activity_id, current_provider.id, deadline_data.new_deadline)

    if result is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not authorized to update this activity")
    if result == "invalid_deadline":
        raise HTTPException(status_code=400, detail="Deadline must be in the future")

    return result

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from schemas import ActivityCreate, ActivityResponse, ActivityUpdate, ActivityDeadlineUpdate
from models.models import Provider, Notification, Subscription
from auth_utils import get_current_provider
from database import get_db
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/activities")

# ✅ 활동 등록
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

# ✅ 활동 목록 조회
@router.get("/", response_model=list[ActivityResponse])
def read_activities(
    region: Optional[str] = None,
    interest: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_activities_with_filter(db, region, interest)

# ✅ 활동 상세 조회
@router.get("/{activity_id}", response_model=ActivityResponse)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = crud.get_activity_by_id(db, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다.")
    return db_activity

# ✅ 활동 수정
@router.put("/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, update: ActivityUpdate, db: Session = Depends(get_db)):
    updated = crud.update_activity(db, activity_id, update)
    if not updated:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다.")
    return updated

# ✅ 활동 삭제
@router.delete("/{activity_id}", response_model=ActivityResponse)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_activity(db, activity_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다.")
    return deleted

# ✅ 모집 인원 미달 활동 조회
@router.get("/insufficient")
def get_insufficient_activities(db: Session = Depends(get_db)):
    return crud.get_insufficient_activities(db)

# ✅ 활동 확정
@router.patch("/{activity_id}/confirm", response_model=ActivityResponse)
def confirm_activity(
    activity_id: int,
    current_provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db)
):
    result = crud.confirm_activity(db, activity_id, current_provider.id)

    if result is None:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다.")
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="해당 활동을 확정할 권한이 없습니다.")
    if result == "already_confirmed":
        raise HTTPException(status_code=400, detail="이미 확정된 활동입니다.")
    if result == "not_enough_participants":
        raise HTTPException(status_code=400, detail="참여 인원이 부족하여 확정할 수 없습니다.")

    # ✅ 사용자에게 알림 발송
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

# ✅ 활동 모집 취소
@router.patch("/{activity_id}/cancel", response_model=ActivityResponse)
def cancel_activity(
    activity_id: int,
    current_provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db)
):
    result = crud.cancel_activity(db, activity_id, current_provider.id)

    if result is None:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다.")
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="해당 활동을 취소할 권한이 없습니다.")

    return result

# ✅ 활동 모집 마감일 수정
@router.patch("/{activity_id}/deadline", response_model=ActivityResponse)
def update_deadline(
    activity_id: int,
    deadline_data: ActivityDeadlineUpdate,
    current_provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db)
):
    result = crud.update_activity_deadline(db, activity_id, current_provider.id, deadline_data.new_deadline)

    if result is None:
        raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다.")
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="해당 활동의 마감일을 수정할 권한이 없습니다.")
    if result == "invalid_deadline":
        raise HTTPException(status_code=400, detail="마감일은 현재 시간 이후로 설정해야 합니다.")

    return result

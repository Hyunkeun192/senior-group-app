from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from schemas import ActivityCreate, ActivityResponse, ActivityUpdate
from models.models import Provider, Notification, Subscription
from auth_utils import get_current_provider
from datetime import datetime
from typing import Optional  # ✅ 추가
from schemas import ActivityDeadlineUpdate  # ✅ 추가

router = APIRouter()

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 활동 등록 API
@router.post("/activities/", response_model=ActivityResponse)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_provider: Provider = Depends(get_current_provider)  # ✅ 현재 로그인 업체 정보 추출
):
    if not current_provider.is_approved:  # ✅ 승인되지 않은 경우 차단
        raise HTTPException(status_code=403, detail="승인되지 않은 업체는 활동을 등록할 수 없습니다.")

    # ✅ 강제적으로 provider_id를 현재 로그인한 provider로 설정
    activity.provider_id = current_provider.id

    return crud.create_activity(db, activity)


# ✅ 활동 전체 조회 API (필터링 기능 추가)
@router.get("/activities/", response_model=list[ActivityResponse])
def read_activities(
    region: Optional[str] = None,
    interest: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_activities_with_filter(db, region, interest)

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

# ✅ 활동 확정 + 사용자 알림 API
@router.patch("/activities/{activity_id}/confirm", response_model=ActivityResponse)
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

    # ✅ 알림 전송 로직이 여기에 있다면, 그 뒤에 꼭 리턴!
    return result  # ✅ 이 줄 추가!


# ✅ 활동 취소 API
@router.patch("/activities/{activity_id}/cancel", response_model=ActivityResponse)
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

# ✅ 모집 마감일 수정 API
@router.patch("/activities/{activity_id}/deadline", response_model=ActivityResponse)
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
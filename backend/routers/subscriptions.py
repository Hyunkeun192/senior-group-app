from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import SubscriptionCreate, SubscriptionResponse
import crud
from auth_utils import get_current_user
from database import get_db
from models.models import Activity, Subscription, Notification

router = APIRouter()

# ✅ 활동 신청
@router.post("/subscriptions/", response_model=SubscriptionResponse)
def subscribe_activity(
    sub: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        new_subscription = crud.create_subscription(db, user_id=current_user.id, activity_id=sub.activity_id)

        activity = db.query(Activity).filter(Activity.id == sub.activity_id).first()
        if not activity:
            raise HTTPException(status_code=404, detail="활동을 찾을 수 없습니다.")

        # ✅ 최소 인원 이상이면 provider에게 알림 (중복 방지)
        total_participants = db.query(Subscription).filter(
            Subscription.activity_id == sub.activity_id
        ).count()

        if total_participants >= activity.min_participants and activity.status != "confirmed":
            existing_notification = db.query(Notification).filter(
                Notification.provider_id == activity.provider_id,
                Notification.message.contains(activity.title),
                Notification.is_read == False
            ).first()

            if not existing_notification:
                notification = Notification(
                    provider_id=activity.provider_id,
                    message=f"'{activity.title}' 활동이 최소 인원에 도달했습니다. 확정해주세요!",
                    is_read=False
                )
                db.add(notification)
                db.commit()

        return new_subscription

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="이미 신청한 활동입니다.")

# ✅ 내 신청 목록 조회
@router.get("/subscriptions/me", response_model=list[SubscriptionResponse])
def get_my_subscriptions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_user_subscriptions(db, user_id=current_user.id)

# ✅ 신청 취소
@router.delete("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted = crud.delete_subscription(db, subscription_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="신청 내역을 찾을 수 없습니다.")
    return deleted

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import SubscriptionCreate, SubscriptionResponse  # ✅ 직접 import로 변경
import crud
from database import SessionLocal
from routers.auth_utils import get_current_user
from models.models import Activity, Subscription, Notification, User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 활동 신청 API
@router.post("/subscriptions/", response_model=SubscriptionResponse)
def subscribe_activity(
    sub: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        new_subscription = crud.create_subscription(db, user_id=current_user.id, activity_id=sub.activity_id)

        total_participants = db.query(Subscription).filter(Subscription.activity_id == sub.activity_id).count()
        activity = db.query(Activity).filter(Activity.id == sub.activity_id).first()

        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        if total_participants >= activity.min_participants and activity.status != "confirmed":
            activity.status = "confirmed"
            db.commit()

            participants = db.query(Subscription).filter(Subscription.activity_id == sub.activity_id).all()
            for participant in participants:
                notification = Notification(
                    user_id=participant.user_id,
                    message=f"활동 '{activity.title}'이 확정되었습니다!",
                    is_read=False
                )
                db.add(notification)

            provider = db.query(User).filter(User.id == activity.provider_id).first()
            if provider:
                notification = Notification(
                    user_id=provider.id,
                    message=f"활동 '{activity.title}'이 확정되었습니다! 참가자 모집이 완료되었습니다.",
                    is_read=False
                )
                db.add(notification)

            db.commit()

        return new_subscription

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="You have already subscribed to this activity")

# ✅ (수정됨) 현재 사용자 신청 목록 조회 API → 경로 변경
@router.get("/subscriptions/me", response_model=list[SubscriptionResponse])  # ⬅ /subscriptions/ → /subscriptions/me
def get_my_subscriptions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_user_subscriptions(db, user_id=current_user.id)

# ✅ 신청 취소 API
@router.delete("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted = crud.delete_subscription(db, subscription_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return deleted

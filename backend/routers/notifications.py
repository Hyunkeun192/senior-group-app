from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models.models import Notification
from schemas import NotificationCreate, NotificationResponse
from auth_utils import get_current_user, get_current_provider  # ✅ 경로 수정

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

# 1️⃣ 알림 생성 API
@router.post("/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    new_notification = Notification(
        user_id=notification.user_id,
        provider_id=notification.provider_id,  # ✅ optional
        message=notification.message,
        created_at=datetime.utcnow()
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification

# 2️⃣ 사용자 본인 알림 조회
@router.get("/me", response_model=list[NotificationResponse])
def get_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()
    return notifications

# 3️⃣ 알림 읽음 처리
@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification

# ✅ 4️⃣ provider 본인 알림 조회 (토큰 인증 보호됨)
@router.get("/provider/me", response_model=list[NotificationResponse])
def get_notifications_for_provider_me(
    db: Session = Depends(get_db),
    current_provider=Depends(get_current_provider)
):
    notifications = db.query(Notification).filter(
        Notification.provider_id == current_provider.id
    ).order_by(Notification.created_at.desc()).all()

    return notifications

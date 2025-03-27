from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

# ✅ import 방식 유지
from database import get_db
from models.models import Notification
from schemas import NotificationCreate, NotificationResponse
from auth_utils import get_current_user

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

# 1️⃣ 알림 생성 API
@router.post("/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    new_notification = Notification(
        user_id=notification.user_id,
        message=notification.message,
        created_at=datetime.utcnow()
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification

# 2️⃣ 현재 사용자 알림 조회 API
@router.get("/me", response_model=list[NotificationResponse])
def get_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # ✅ current_user는 dict가 아니라 User 객체이므로 .id 접근
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()
    return notifications

# 3️⃣ 알림 읽음 처리 API
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

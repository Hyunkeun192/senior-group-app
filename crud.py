from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
import schemas
from models.models import User, Provider, Activity, Payment, Subscription
from schemas import UserBase, UserCreate  # ✅ 명확하게 import
import models

# ✅ 비밀번호 해싱을 위한 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """비밀번호를 bcrypt로 해싱"""
    return pwd_context.hash(password)

# ✅ 사용자 계정 생성 (비밀번호 해싱 적용)
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password_hash=hashed_password,
        location=user.location,
        interests=user.interests
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ✅ 관리자 계정 생성 (비밀번호 해싱 적용)
def create_admin(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_admin = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password_hash=hashed_password,
        location=user.location,
        interests=user.interests,
        is_admin=True
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

# ✅ 사용자 조회
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# ✅ 업체 이메일로 조회
def get_provider_by_email(db: Session, email: str):
    return db.query(Provider).filter(Provider.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# ✅ 사용자 수정
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# ✅ 사용자 삭제
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

# ✅ 업체 승인
def approve_provider(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        return None
    provider.is_approved = True
    db.commit()
    return provider

# ✅ 관리자 통계
def get_admin_stats(db: Session):
    return {
        "total_users": db.query(User).count(),
        "total_providers": db.query(Provider).count(),
        "total_activities": db.query(Activity).count(),
        "total_payments": db.query(Payment).count()
    }

# ✅ 활동 생성
def create_activity(db: Session, activity_data: schemas.ActivityCreate):
    db_activity = Activity(
        title=activity_data.title,
        description=activity_data.description,
        provider_id=activity_data.provider_id,
        min_participants=activity_data.min_participants,
        price_per_person=activity_data.price_per_person,
        status=activity_data.status if activity_data.status else "pending"
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

# ✅ 활동 조회
def get_activities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Activity).offset(skip).limit(limit).all()

def get_activity_by_id(db: Session, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()

# ✅ 활동 수정
def update_activity(db: Session, activity_id: int, activity_update: schemas.ActivityUpdate):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not db_activity:
        return None
    for key, value in activity_update.dict(exclude_unset=True).items():
        setattr(db_activity, key, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity

# ✅ 활동 삭제 (status 변경)
def delete_activity(db: Session, activity_id: int):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not db_activity:
        return None
    db_activity.status = "inactive"
    db.commit()
    db.refresh(db_activity)
    return db_activity

# ✅ 업체 등록
def create_provider(db: Session, provider: schemas.ProviderCreate):
    db_provider = Provider(
        name=provider.name,
        contact=provider.contact,
        service_area=provider.service_area
    )
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

# ✅ 구독 생성
def create_subscription(db: Session, user_id: int, activity_id: int):
    new_subscription = Subscription(
        user_id=user_id,
        activity_id=activity_id,
        status="pending"
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

# ✅ 사용자 구독 조회
def get_user_subscriptions(db: Session, user_id: int):
    return db.query(Subscription).filter(Subscription.user_id == user_id).all()

# crud.py

def get_provider_activities_with_counts(db: Session, provider_id: int):
    from models import Activity, Subscription
    results = (
        db.query(
            Activity.id,
            Activity.title,
            Activity.status,
            func.count(Subscription.id).label("current_participants")
        )
        .outerjoin(Subscription, Activity.id == Subscription.activity_id)
        .filter(Activity.provider_id == provider_id)
        .group_by(Activity.id)
        .all()
    )

    return [
        {
            "activity_id": r.id,
            "title": r.title,
            "status": r.status,
            "current_participants": r.current_participants
        }
        for r in results
    ]

# ✅ 활동별 현재 참여자 수를 조회하는 함수 (provider 대시보드용)
def get_activity_participants_for_provider(db: Session, provider_id: int):
    return (
        db.query(
            models.Activity.id.label("activity_id"),
            models.Activity.title,
            func.count(models.Subscription.id).label("participants_count")
        )
        .join(models.Subscription, models.Activity.id == models.Subscription.activity_id)
        .filter(models.Activity.provider_id == provider_id)
        .group_by(models.Activity.id)
        .all()
    )

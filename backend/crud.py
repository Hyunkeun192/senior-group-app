from sqlalchemy.orm import Session
from sqlalchemy import func
from auth_utils import get_password_hash  # ✅ 외부 모듈에서 가져오기
from models.models import User, Provider, Activity, Payment, Subscription, Notification, CustomInterest
import schemas
from datetime import datetime, timezone
from typing import Optional, List  # ✅ 선택형 타입 사용을 위한 필수 import

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
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

def create_admin(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
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

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_provider_by_email(db: Session, email: str):
    return db.query(Provider).filter(Provider.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

def approve_provider(db: Session, provider_id: int):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        return None
    provider.is_approved = True
    db.commit()
    return provider

def get_admin_stats(db: Session):
    return {
        "total_users": db.query(User).count(),
        "total_providers": db.query(Provider).count(),
        "total_activities": db.query(Activity).count(),
        "total_payments": db.query(Payment).count()
    }

def get_activities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Activity).offset(skip).limit(limit).all()

def get_activity_by_id(db: Session, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()

def update_activity(db: Session, activity_id: int, activity_update: schemas.ActivityUpdate):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not db_activity:
        return None
    for key, value in activity_update.dict(exclude_unset=True).items():
        setattr(db_activity, key, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: int):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not db_activity:
        return None
    db_activity.status = "inactive"
    db.commit()
    db.refresh(db_activity)
    return db_activity

def create_provider(db: Session, provider: schemas.ProviderCreate):
    hashed_pw = pwd_context.hash(provider.password)
    db_provider = Provider(
        name=provider.name,
        email=provider.email,
        phone=provider.phone,
        password_hash=hashed_pw,
        service_area=provider.service_area,
        service_name=provider.service_name,
        is_business=provider.is_business,
        business_registration_number=provider.business_registration_number,
        created_at=datetime.utcnow()
    )
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


# ✅ 최소 인원 도달 시 provider에게 알림 전송
def notify_provider_when_minimum_reached(db: Session, activity_id: int):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity or activity.status == "confirmed":
        return

    participant_count = db.query(Subscription).filter(Subscription.activity_id == activity_id).count()
    if participant_count >= activity.min_participants:
        provider_id = activity.provider_id
        message = f"'{activity.title}' 활동에 최소 인원이 모집되었습니다. 확정해주세요!"
        notification = Notification(
            provider_id=provider_id,
            message=message,
            is_read=False
        )
        db.add(notification)
        db.commit()

# ✅ 구독 생성 + 최소 인원 도달 시 알림 전송
def create_subscription(db: Session, user_id: int, activity_id: int):
    new_subscription = Subscription(
        user_id=user_id,
        activity_id=activity_id,
        status="pending"
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    notify_provider_when_minimum_reached(db, activity_id=activity_id)

    return new_subscription

def get_user_subscriptions(db: Session, user_id: int):
    return db.query(Subscription).filter(Subscription.user_id == user_id).all()

def get_provider_activities_with_counts(db: Session, provider_id: int):
    results = (
        db.query(
            Activity.id,
            Activity.title,
            Activity.status,
            Activity.min_participants, 
            Activity.deadline,  # ✅ 이 줄 추가!
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
        "current_participants": r.current_participants,
        "min_participants": r.min_participants,  # ✅ 쉼표로 꼭 구분!
        "deadline": r.deadline   # ✅ 이 줄 추가!
        }
        for r in results
    ]

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

def get_activities_by_provider(db: Session, provider_id: int):
    return db.query(Activity).filter(Activity.provider_id == provider_id).all()

# ✅ 활동 확정 처리
from fastapi import HTTPException  # 이미 되어 있을 가능 있음

def confirm_activity(db: Session, activity_id: int, provider_id: int):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    if activity.provider_id != provider_id:
        raise HTTPException(status_code=403, detail="Not authorized to confirm this activity")

    if activity.status == "confirmed":
        raise HTTPException(status_code=400, detail="Activity already confirmed")

    current_subs = db.query(Subscription).filter(Subscription.activity_id == activity_id).count()
    if current_subs < activity.min_participants:
        raise HTTPException(status_code=400, detail="Not enough participants to confirm")

    activity.status = "confirmed"
    db.commit()
    db.refresh(activity)

    # ✅ 사용자에게 알림 전송
    notify_users_of_confirmed_activity(
        db,
        activity_id,
        f"활동 '{activity.title}'이(가) 확정되었습니다. 결제할 수 있습니다."
    )

    return activity



# ✅ 사용자들에게 활동 확정 알림 전송
def notify_users_of_confirmed_activity(db: Session, activity_id: int, message: str):
    user_ids = db.query(Subscription.user_id).filter(Subscription.activity_id == activity_id).all()
    for (user_id,) in user_ids:
        notification = Notification(
            user_id=user_id,
            message=message,
            is_read=False
        )
        db.add(notification)
    db.commit()

def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = Activity(
        title=activity.title,
        description=activity.description,
        provider_id=activity.provider_id,
        min_participants=activity.min_participants,
        price_per_person=activity.price_per_person,
        interest_category=activity.interest_category,  # ✅
        interest_subcategory=activity.interest_subcategory,  # ✅
        deadline=activity.deadline,  # ✅ 이 줄 추가!
        region=activity.region,  # ✅ 이 줄이 꼭 있어야 함!
        status=activity.status
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def get_activities_with_filter(db: Session, region: Optional[str] = None, interest: Optional[str] = None):
    query = db.query(Activity)

    if region:
        query = query.join(Provider).filter(Provider.service_area.contains(region))
    if interest:
        query = query.filter(
            (Activity.interest_category.contains(interest)) |
            (Activity.interest_subcategory.contains(interest))
        )

    return query.all()

# ✅ 모집 마감일 수정 함수
def update_activity_deadline(db: Session, activity_id: int, provider_id: int, new_deadline: datetime):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    print("🔎 활동의 provider_id:", activity.provider_id)
    print("🔐 현재 로그인한 provider_id:", provider_id)

    if not activity:
        return None

    if int(activity.provider_id) != int(provider_id):
        print("❌ provider_id 불일치!")
        return "unauthorized"

    if new_deadline <= datetime.utcnow().replace(tzinfo=timezone.utc):
        return "invalid_deadline"

    activity.deadline = new_deadline
    db.commit()
    db.refresh(activity)
    return activity

# ✅ 사용자 입력 관심사 저장
def create_custom_interest(db: Session, interest: schemas.CustomInterestCreate):
    new_interest = CustomInterest(
        user_id=interest.user_id,
        value=interest.value
    )
    db.add(new_interest)
    db.commit()
    db.refresh(new_interest)
    return new_interest

# ✅ 모든 사용자 입력 관심사 조회
def get_all_custom_interests(db: Session):
    return db.query(CustomInterest).all()

# ✅ 유사 관심사들을 그룹으로 통합
def group_and_approve_interests(db: Session, interest_ids: List[int], group_id: int):
    interests = db.query(CustomInterest).filter(CustomInterest.id.in_(interest_ids)).all()
    for interest in interests:
        interest.status = "approved"
        interest.group_id = group_id
    db.commit()
    return interests

# ✅ 처리되지 않은 주관식 관심사 조회
def get_unprocessed_custom_interests(db: Session):
    return db.query(models.CustomInterest).filter(
        models.CustomInterest.status == "pending"
    ).all()

# crud.py 파일 맨 아래쯤에 추가해줘

def delete_subscription(db: Session, subscription_id: int, user_id: int):
    subscription = db.query(models.models.Subscription).filter(
        models.models.Subscription.id == subscription_id,
        models.models.Subscription.user_id == user_id
    ).first()

    if not subscription:
        return None

    db.delete(subscription)
    db.commit()
    return subscription

def cancel_activity(db: Session, activity_id: int, provider_id: int):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return None
    if activity.provider_id != provider_id:
        return "unauthorized"
    activity.status = "cancelled"
    db.commit()
    db.refresh(activity)
    return activity

def get_users_with_filters(db: Session, search: str = "", sort: str = "created_at", order: str = "desc"):
    query = db.query(User)

    if search:
        query = query.filter(User.name.contains(search) | User.email.contains(search))

    if sort == "created_at":
        sort_column = User.created_at
    elif sort == "email":
        sort_column = User.email
    else:
        sort_column = User.name

    sort_column = sort_column.desc() if order == "desc" else sort_column.asc()
    return query.order_by(sort_column).all()

def get_providers_with_filters(db: Session, search: str = "", sort: str = "created_at", order: str = "desc"):
    query = db.query(Provider)

    if search:
        query = query.filter(Provider.name.contains(search) | Provider.email.contains(search))

    if sort == "created_at":
        sort_column = Provider.created_at
    elif sort == "email":
        sort_column = Provider.email
    else:
        sort_column = Provider.name

    sort_column = sort_column.desc() if order == "desc" else sort_column.asc()
    return query.order_by(sort_column).all()

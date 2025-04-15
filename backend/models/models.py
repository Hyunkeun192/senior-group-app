from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.orm import relationship, Session
from models.base import Base
from datetime import datetime
from typing import Optional
import models  # ✅ 관계 매핑용 import




# ✅ 사용자 테이블
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=True)
    password_hash = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    interests = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

# ✅ 업체 테이블 (수정됨)
class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255))  # ✅ 이 줄 추가!
    service_area = Column(String(100), nullable=False)
    service_name = Column(String(100), nullable=False)
    is_business = Column(Boolean, default=False)
    business_registration_number = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_approved = Column(Boolean, default=False)  # ✅ 업체 승인 여부 필드 추가

# ✅ 결제 테이블
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    activity = relationship("Activity")

# ✅ 활동 신청(구독) 테이블
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    activity = relationship("Activity")

# ✅ 알림 테이블
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

# ✅ 수정된 Activity 클래스 (마감일 컬럼 추가됨)
class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    min_participants = Column(Integer, nullable=False)
    price_per_person = Column(Float, nullable=False)
    interest_category = Column(String(100), nullable=True)
    interest_subcategory = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)  # ✅ 이 줄을 새로 추가!
    status = Column(String(50), default="pending", nullable=False)
    deadline = Column(DateTime, nullable=True)  # ✅ 모집 마감일 컬럼 추가
    created_at = Column(DateTime, default=datetime.utcnow)

    provider = relationship("Provider")

# ✅ 사용자 주관식 관심사 테이블 (신규 추가)
class CustomInterest(Base):
    __tablename__ = "custom_interests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # ✅ null 허용
    value = Column(String(100), nullable=False)
    status = Column(String(20), default="pending")
    group_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ✅ 관리자 테이블 (신규 추가)
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50), nullable=False)

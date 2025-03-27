from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.orm import relationship, Session
from models.base import Base
import datetime
import models  # ✅ Subscription 등 관계 매핑을 위한 import (필요 시)

# ✅ 사용자 테이블
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=True)  # ✅ phone 필드 추가
    password_hash = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    interests = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False)  # ✅ 관리자 여부 필드 추가
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


# ✅ 업체 테이블
class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # 실제 사람 이름
    email = Column(String(100), unique=True, nullable=False)  # 로그인용 이메일
    phone = Column(String(50), nullable=False)  # 기존 contact
    password_hash = Column(String(255), nullable=False)
    service_area = Column(String(255), nullable=False)
    service_name = Column(String(100), nullable=False)  # 업체 이름
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# ✅ 활동 테이블
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    min_participants = Column(Integer, nullable=False)
    price_per_person = Column(Float, nullable=False)
    status = Column(String(50), default="pending", nullable=False)  # ✅ 상태 필드 추가
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    provider = relationship("Provider")


# ✅ 결제 테이블
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")  # ✅ 기본값 설정
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")
    activity = relationship("Activity")


# ✅ 활동 신청(구독) 테이블
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")
    activity = relationship("Activity")


# ✅ 알림 테이블
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="notifications")

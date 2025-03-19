from sqlalchemy import Column, Integer, String, Enum, JSON, TIMESTAMP, func
from app.database import Base  # ✅ database 모듈의 경로 수정

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    location = Column(String(100), nullable=True)
    interests = Column(JSON, nullable=True)
    role = Column(Enum("user", "provider", "admin", name="user_role"), default="user")

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)  # ✅ created_at 추가

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    business_name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    contact_phone = Column(String(20), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)  # ✅ created_at 추가



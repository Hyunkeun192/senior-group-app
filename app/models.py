from sqlalchemy import Column, Integer, String, JSON, Enum, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

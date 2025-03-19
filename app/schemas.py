from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

# ✅ 사용자 응답 스키마
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[Dict[str, str]] = None
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

# ✅ 사용자 생성 요청 스키마
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[List[str]] = None
    role: Optional[str] = "user"

# ✅ 사용자 로그인 요청 스키마 (새로 추가)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ✅ 업체 응답 스키마
class ProviderResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    service_area: Optional[str] = None
    services: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True

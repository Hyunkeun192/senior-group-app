from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ✅ 사용자 관련 모델
class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True  # ✅ SQLAlchemy 모델 변환 가능

    model_config = {  # ✅ Swagger 예시용 추가 (스키마 오류 방지)
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "James Smith",
                    "email": "james.smith@gmail.com",
                    "phone": "+1-202-555-0173",
                    "location": "New York",
                    "interests": "Yoga, Hiking"
                }
            ]
        }
    }

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[str] = None

# ✅ 업체 관련 모델
class ProviderBase(BaseModel):
    name: str
    contact: str
    service_area: str

class ProviderCreate(ProviderBase):
    pass

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    service_area: Optional[str] = None

class ProviderResponse(ProviderBase):
    id: int

    class Config:
        orm_mode = True

# ✅ 활동 관련 모델
class ActivityBase(BaseModel):
    title: str
    description: str
    provider_id: int
    min_participants: int
    price_per_person: float

class ActivityCreate(ActivityBase):
    status: Optional[str] = "pending"

class ActivityResponse(ActivityBase):
    id: int
    status: str

    class Config:
        orm_mode = True

# ✅ 결제 관련 모델
class PaymentBase(BaseModel):
    activity_id: int
    amount: float

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    user_id: int
    status: str

    class Config:
        orm_mode = True

# ✅ 로그인 토큰 요청/응답 모델
class TokenRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# ✅ 구독(참여 신청) 관련 모델
class SubscriptionCreate(BaseModel):
    activity_id: int

class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    activity_id: int
    status: str

    class Config:
        orm_mode = True

# ✅ 알림(Notification) 모델
class NotificationCreate(BaseModel):
    user_id: int
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True

# ✅ 활동(모임) 수정용 모델
class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    provider_id: Optional[int] = None
    min_participants: Optional[int] = None
    price_per_person: Optional[float] = None
    status: Optional[str] = None

# 추가
class ProviderLogin(BaseModel):
    email: str
    password: str

# ✅ 활동별 참여자 수 응답 모델 (provider 대시보드용)
class ActivityParticipantsResponse(BaseModel):
    activity_id: int
    title: str
    participants_count: int

    class Config:
        orm_mode = True

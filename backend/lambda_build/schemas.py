from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from datetime import date



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
        orm_mode = True

    model_config = {
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
    email: str
    phone: str
    service_area: str
    service_name: str

class ProviderCreate(ProviderBase):
    password: str  # ✅ 입력 받을 때만 필요
    is_business: Optional[bool] = False  # ✅ 추가
    business_registration_number: Optional[str] = None  # ✅ 추가

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
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
    interest_category: Optional[str] = None  # ✅ 추가
    interest_subcategory: Optional[str] = None  # ✅ 추가
    deadline: Optional[date] = None  # ✅ 여기에 추가 필요!
    region: Optional[str] = None  # ✅ 이 줄 추가

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
    user_id: Optional[int] = None
    provider_id: Optional[int] = None  # ✅ 추가
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    provider_id: Optional[int] = None  # ✅ 추가
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

# ✅ 로그인용 모델
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

# ✅ 모집 마감일 수정용 요청 모델
class ActivityDeadlineUpdate(BaseModel):
    new_deadline: datetime

# ✅ 사용자 주관식 관심사 생성 요청 모델
class CustomInterestCreate(BaseModel):
    value: str

# ✅ 사용자 주관식 관심사 응답 모델
class CustomInterestResponse(BaseModel):
    id: int
    user_id: int
    value: str
    status: str
    group_id: Optional[int] = None
    created_at: Optional[datetime] = None  # created_at은 nullable 허용

    class Config:
        orm_mode = True

class GroupInterestsRequest(BaseModel):
    interest_ids: List[int]
    group_id: int


# ⬇️ 관리자 로그인 요청 스키마
class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str

# ⬇️ 관리자 로그인 응답 스키마
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ✅ 사용자 주관식 관심사 조회용 스키마
class CustomInterestOut(BaseModel):
    id: int
    user_id: int
    value: str
    status: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    location: Optional[str]
    interested_activities: Optional[List[str]] = []
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

# 이미 있을 수 있음, 없으면 추가
class ProviderOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    service_area: str
    service_name: str
    is_business: bool
    business_registration_number: Optional[str]
    is_approved: bool  # ✅ 승인 여부 추가

    class Config:
        orm_mode = True

class InterestCreate(BaseModel):
    category: str
    subcategory: str

class InterestOut(BaseModel):
    id: int
    category: str
    subcategory: str

    class Config:
        orm_mode = True  # ✅ 꼭 있어야 함

class AdminSignupRequest(BaseModel):
    email: EmailStr
    password: str

# ✅ 관리자 - 승인 대기 업체 요약 정보 모델
class ProviderPendingResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    service_area: str
    service_name: str
    is_business: bool
    business_registration_number: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

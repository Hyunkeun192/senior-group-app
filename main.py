import sys
import os

# ✅ backend 경로를 sys.path에 강제 추가 (import 문제 해결)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from mangum import Mangum

# ✅ import 방식 변경 (절대 경로 → 상대 경로)
from routers.users import router as users_router
from routers.auth import router as auth_router
from routers.providers import router as providers_router
from routers.activities import router as activities_router
from routers.subscriptions import router as subscriptions_router
from routers.notifications import router as notifications_router
from routers.admin import router as admin_router  # ✅ 관리자 라우터 추가
from routers.payments import router as payments_router  # ✅ 결제 라우터 추가

from database import engine
from models.models import Base
import schemas  # ✅ Swagger에서 참조할 수 있도록 명시적으로 import
from schemas import UserCreate, UserResponse  # ✅ 명시적으로 추가

app = FastAPI()

# ✅ DB 테이블 생성
Base.metadata.create_all(bind=engine)

# ✅ 라우터 등록
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(providers_router)
app.include_router(activities_router)
app.include_router(subscriptions_router)
app.include_router(notifications_router)  # ✅ 알림 라우터 추가
app.include_router(admin_router)  
app.include_router(payments_router)  # ✅ 결제 API 추가

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

# ✅ Swagger UI에서 Bearer Token을 사용하도록 설정 (Authorize 버튼 추가)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Senior Group Matching API",
        version="1.0.0",
        description="API documentation for Senior Group Matching Service",
        routes=app.routes,
    )
    openapi_schema["components"] = {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return openapi_schema  # ✅ 기존 코드의 오류 수정 (함수 실행이 아니라 함수 자체를 설정)

# ✅ Swagger UI에서 Bearer Token을 인식하도록 반영
app.openapi = custom_openapi  # ✅ 이제 활성화

handler = Mangum(app)

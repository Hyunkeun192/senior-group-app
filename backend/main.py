import sys
import os

# ✅ backend 경로를 sys.path에 강제 추가 (import 문제 해결)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware  # ✅ CORS 미들웨어 추가
from mangum import Mangum

# ✅ import 방식 변경 (절대 경로 → 상대 경로)
from routers.users import router as users_router
from routers.auth import router as auth_router
from routers.providers import router as providers_router
from routers.activities import router as activities_router
from routers.subscriptions import router as subscriptions_router
from routers.notifications import router as notifications_router
from routers.admin_auth import router as admin_auth_router
from routers.admin import router as admin_router
from routers.payments import router as payments_router

from database import engine
from models.models import Base
import schemas
from schemas import UserCreate, UserResponse

app = FastAPI()

# ✅ CORS 설정: 프론트엔드(React)와 연동 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB 테이블 생성
Base.metadata.create_all(bind=engine)

# ✅ 라우터 등록
app.include_router(users_router)
app.include_router(auth_router, prefix="/auth")  # 🔥 prefix 추가
app.include_router(admin_auth_router)
app.include_router(providers_router)
app.include_router(activities_router)
app.include_router(subscriptions_router)
app.include_router(notifications_router)
app.include_router(admin_router)
app.include_router(payments_router)

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
    return openapi_schema

# ✅ Swagger UI에서 Bearer Token을 인식하도록 반영
app.openapi = custom_openapi

# ✅ AWS Lambda 연동용 핸들러
handler = Mangum(app)

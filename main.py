from fastapi import FastAPI
from app.routers import users, providers  # ✅ 중복된 import 정리
from app.database import Base, engine  # ✅ DB 테이블 자동 생성 추가

# FastAPI 앱 생성
app = FastAPI(
    title="Senior Group App",
    description="시니어 레저 및 취미 매칭 서비스 API",
    version="1.0.0",
)

# 데이터베이스 테이블 자동 생성 (서버 시작 시)
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(providers.router, prefix="/providers", tags=["Providers"])

# 기본 페이지
@app.get("/")
def read_root():
    return {"message": "Welcome to Senior Group App API!"}

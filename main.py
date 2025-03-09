from fastapi import FastAPI, Body, Request
from pydantic import BaseModel
from typing import Optional
import crud  # ✅ CRUD 함수 불러오기

app = FastAPI()

# ✅ 사용자 데이터 모델 정의
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    role: Optional[str] = "user"  # 기본 역할은 "user"

# ✅ 업체 데이터 모델 정의
class ProviderCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    description: str

# ✅ 기본 API 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI & MySQL!"}

# ✅ MySQL 연결 테스트 API
@app.get("/test-db")
def test_db_connection():
    connection = crud.get_connection()
    if connection:
        crud.release_connection(connection)
        return {"message": "✅ Database connection successful!"}
    else:
        return {"error": "❌ Failed to connect to the database"}

# ✅ 사용자 정보 수정 API (PUT 요청 → JSON 데이터 확실히 받도록 수정됨)
@app.put("/users/{user_id}")
async def modify_user(user_id: int, user: UserCreate):
    return crud.update_user(user_id, user)  # 이제 UserCreate 객체를 전달

# 모든 사용자 조회 API
@app.get("/users")
def get_users():
    users = crud.get_all_users()
    return {"users": users}

# 특정 사용자 조회 API
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = crud.get_user_by_id(user_id)
    if user:
        return {"user": user}
    return {"error": "User not found"}

# 사용자 추가 API
@app.post("/users")
def add_user(name: str, email: str, password: str, phone: str, role: str = "user"):
    return crud.create_user(name, email)

# 사용자 정보 수정 API
@app.put("/users/{user_id}")
def modify_user(user_id: int, name: str, email: str, phone: str, role: str):
    return crud.update_user(user_id, name, email, phone, role)

# 사용자 삭제 API
@app.delete("/users/{user_id}")
def remove_user(user_id: int):
    return crud.delete_user(user_id)

# 모든 업체 조회 API
@app.get("/providers")
def get_providers():
    providers = crud.get_all_providers()
    return {"providers": providers}

# 특정 업체 조회 API
@app.get("/providers/{provider_id}")
def get_provider(provider_id: int):
    provider = crud.get_provider_by_id(provider_id)
    if provider:
        return {"provider": provider}
    return {"error": "Provider not found"}

# 업체 추가 API
@app.post("/providers")
def add_provider(name: str, email: str, phone: str, address: str, description: str):
    return crud.create_provider(name, email, phone, address, description)

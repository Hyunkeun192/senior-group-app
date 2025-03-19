from fastapi import FastAPI
from app.routers import users, providers  # 추가된 라우터 가져오기

app = FastAPI()

# 라우터 등록
app.include_router(users.router)
app.include_router(providers.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Senior Group App!"}

from fastapi import FastAPI
from app.routers import users

app = FastAPI()

# API 라우터 등록
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


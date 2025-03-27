import pymysql
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

# 환경 변수 로드
load_dotenv()

# ✅ 환경 변수에서 DB 정보 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL이 설정되지 않았습니다. .env 파일을 확인하세요.")
else:
    print(f"✅ DATABASE_URL 확인: {DATABASE_URL}")

# ✅ SQLAlchemy 엔진 설정
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ✅ 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ 의존성 주입을 위한 세션 함수 추가
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 데이터베이스 테이블 생성
print("✅ 데이터베이스 테이블 생성 중...")
Base.metadata.create_all(bind=engine)
print("✅ 테이블 생성 완료!")

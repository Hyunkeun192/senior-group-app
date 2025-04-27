# database.py
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

# ✅ 환경 변수 로드
load_dotenv()

# ✅ 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ 환경 변수에서 DB 정보 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("❌ DATABASE_URL이 설정되지 않았습니다. .env 파일을 확인하세요.")
    raise ValueError("DATABASE_URL is not set.")
else:
    logger.info(f"✅ DATABASE_URL 확인: {DATABASE_URL}")

# ✅ SQLAlchemy 엔진 설정
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ✅ 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ 의존성 주입을 위한 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 개발 모드에서만 테이블 자동 생성
if os.getenv("AUTO_CREATE_DB", "false").lower() == "true":
    logger.info("✅ 데이터베이스 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ 테이블 생성 완료!")

logger.info(f"✅ 연결된 DB 주소: {DATABASE_URL}")

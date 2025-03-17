import pymysql
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MySQL 연결 설정
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4"
    )

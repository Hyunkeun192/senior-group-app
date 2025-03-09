import mysql.connector
from mysql.connector import pooling

# MySQL 연결 정보
MYSQL_HOST = "my-mysql-rds.cbi0oiueudvh.ap-northeast-2.rds.amazonaws.com"
MYSQL_USER = "admin"
MYSQL_PASSWORD = "WZVeaytDmf7NqgJ"  # ✅ 실제 비밀번호 입력!
MYSQL_DB = "mydatabase"

# MySQL 커넥션 풀 설정
pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,  # ✅ 커넥션 풀 크기 설정 (필요에 따라 조정 가능)
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)

# 커넥션 풀에서 연결 가져오기
def get_connection():
    try:
        connection = pool.get_connection()
        return connection
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

# 연결 반환 함수 (사용 후 반드시 호출!)
def release_connection(connection):
    try:
        if connection:
            connection.close()  # ✅ 연결을 닫으면 자동으로 반환
    except Exception as e:
        print(f"⚠️ Failed to release connection: {e}")

# 사용자 정보 업데이트 함수
def update_user(user_id: int, name: str, email: str, password: str, phone: str, role: str):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # UPDATE SQL 쿼리 작성
            query = """
                UPDATE users
                SET name = %s, email = %s, password = %s, phone = %s, role = %s
                WHERE id = %s
            """
            
            # 쿼리 실행
            cursor.execute(query, (name, email, password, phone, role, user_id))
            
            # 커밋하여 변경 사항 저장
            connection.commit()
            
            cursor.close()
            return {"message": "✅ User updated successfully!"}
        except Exception as e:
            print(f"❌ Error during updating user: {e}")
            return {"error": "❌ Failed to update user"}
        finally:
            release_connection(connection)
    else:
        return {"error": "❌ Database connection failed"}

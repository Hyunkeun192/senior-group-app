from database import get_connection, release_connection
from pydantic import BaseModel

### ✅ `users` 테이블 CRUD 기능 ###

# ✅ 사용자 데이터 모델 정의
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    role: str = "user"  # 기본 역할은 "user"

# ✅ 사용자 추가 (Create)
def create_user(name: str, email: str):
    connection = get_connection()
    if not connection:
        return {"error": "❌ Failed to connect to the database"}

    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        connection.commit()
        release_connection(connection)
        return {"message": "✅ User created successfully!"}
    except Exception as e:
        return {"error": f"❌ Failed to create user: {e}"}

# ✅ 사용자 정보 수정 (Update)
def update_user(user_id: int, user: UserCreate):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # 이메일 중복 확인
            cursor.execute("SELECT * FROM users WHERE email = %s AND id != %s", (user.email, user_id))
            if cursor.fetchone():
                return {"error": "❌ Duplicate email found. Please choose a different email."}
            
            # UPDATE SQL 쿼리 작성
            query = """
                UPDATE users
                SET name = %s, email = %s, password = %s, phone = %s, role = %s
                WHERE id = %s
            """
            
            # 쿼리 실행
            cursor.execute(query, (user.name, user.email, user.password, user.phone, user.role, user_id))
            
            # 커밋하여 변경 사항 저장
            connection.commit()

            cursor.close()
            return {"message": "✅ User updated successfully!"}
        except Exception as e:
            # 오류 메시지 출력
            print(f"❌ Error during updating user: {e}")
            return {"error": f"❌ Failed to update user: {e}"}
        finally:
            release_connection(connection)
    else:
        return {"error": "❌ Database connection failed"}


# ✅ 사용자 조회 (Read)
def get_user_by_id(user_id: int):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return {"user": result}
            else:
                return {"error": "User not found"}
        except Exception as e:
            return {"error": f"❌ Failed to fetch user: {e}"}
        finally:
            release_connection(connection)
    else:
        return {"error": "❌ Database connection failed"}

# ✅ 모든 사용자 조회 (Read)
def get_all_users():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return {"users": result}
        except Exception as e:
            return {"error": f"❌ Failed to fetch users: {e}"}
        finally:
            release_connection(connection)
    else:
        return {"error": "❌ Database connection failed"}

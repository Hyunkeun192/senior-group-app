from database import get_connection
import hashlib

# 관리자 로그인 (단순 비밀번호 해싱 검증)
def admin_login(username, password):
    conn = get_connection()
    if conn:
        with conn.cursor() as cursor:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            sql = "SELECT * FROM admins WHERE username = %s AND password = %s;"
            cursor.execute(sql, (username, hashed_password))
            admin = cursor.fetchone()
        conn.close()
        if admin:
            return {"message": "Login successful", "admin": admin}
        else:
            return {"error": "Invalid credentials"}
    return {"error": "Database connection failed"}

# 모든 사용자 조회
def get_all_users():
    conn = get_connection()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
        conn.close()
        return users
    return None

# 모든 모임 조회
def get_all_groups():
    conn = get_connection()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM groups;")
            groups = cursor.fetchall()
        conn.close()
        return groups
    return None

# 모든 결제 내역 조회
def get_all_payments():
    conn = get_connection()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM payments;")
            payments = cursor.fetchall()
        conn.close()
        return payments
    return None

# 특정 결제 내역 삭제
def delete_payment(payment_id):
    conn = get_connection()
    if conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM payments WHERE id = %s;"
            cursor.execute(sql, (payment_id,))
            conn.commit()
        conn.close()
        return {"message": "Payment deleted successfully"}
    return {"error": "Failed to delete payment"}

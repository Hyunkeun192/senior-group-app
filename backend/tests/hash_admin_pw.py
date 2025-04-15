# /backend/tests/hash_admin_pw.py

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

plain_password = "admin1234"  # 🔐 원하는 비밀번호로 수정
hashed = pwd_context.hash(plain_password)

print("✅ 복사해서 MySQL에 붙여넣으세요:")
print(hashed)

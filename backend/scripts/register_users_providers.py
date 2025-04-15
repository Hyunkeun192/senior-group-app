import os
import json
import requests

# ✅ 현재 파일 기준 base directory 계산
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))

# ✅ 상대 경로 설정
user_path = os.path.join(PROJECT_ROOT, "backend", "tests", "sample_requests", "sample_users.json")
provider_path = os.path.join(PROJECT_ROOT, "backend", "tests", "sample_requests", "sample_providers.json")

def load_data(user_path, provider_path):
    with open(user_path, "r", encoding="utf-8") as f:
        users = json.load(f)
    with open(provider_path, "r", encoding="utf-8") as f:
        providers = json.load(f)
    return users, providers

def register_users_and_providers(users, providers):
    for u in users:
        try:
            response = requests.post("http://localhost:8000/users/", json=u)
            print("User:", response.status_code, response.text)
        except Exception as e:
            print("User registration error:", e)

    for p in providers:
        try:
            response = requests.post("http://localhost:8000/providers/", json=p)
            print("Provider:", response.status_code, response.text)
        except Exception as e:
            print("Provider registration error:", e)

# ✅ 명시적으로 실행될 때만 실행
if __name__ == "__main__":
    users, providers = load_data(user_path, provider_path)
    register_users_and_providers(users, providers)

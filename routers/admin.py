from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import User, Provider, Activity
from routers.auth_utils import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# ✅ 관리자 권한 확인 함수
def check_admin(user: User):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다.")

# ✅ 1. 업체 등록 승인 API
@router.put("/providers/{provider_id}/approve")
def approve_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)  # ✅ 관리자 권한 확인

    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="업체를 찾을 수 없습니다.")

    provider.is_approved = True  # ✅ 업체 승인
    db.commit()
    return {"message": f"업체 '{provider.name}'가 승인되었습니다."}

# ✅ 2. 사용자 목록 조회 API (관리자만 접근 가능)
@router.get("/users/")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)  # ✅ 관리자 권한 확인

    users = db.query(User).all()

    # ✅ SQLAlchemy 객체를 JSON 변환 (Pydantic 사용)
    users_list = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_admin": user.is_admin
        }
        for user in users
    ]

    return users_list  # ✅ JSON 변환 후 반환



# ✅ 3. 특정 사용자 삭제 API
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)  # ✅ 관리자 권한 확인

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    db.delete(user)
    db.commit()
    return {"message": f"사용자 '{user.name}' 삭제 완료."}

# ✅ 4. 활동 통계 API (관리자 대시보드)
@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)  # ✅ 관리자 권한 확인

    total_users = db.query(User).count()
    total_providers = db.query(Provider).count()
    total_activities = db.query(Activity).count()

    return {
        "total_users": total_users,
        "total_providers": total_providers,
        "total_activities": total_activities
    }

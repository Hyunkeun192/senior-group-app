from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.models import User, Provider, Activity, CustomInterest, Admin, Interest, Notification  # ✅ Admin 모델 추가
from auth_utils import get_current_user, get_current_admin  # ✅ 관리자 인증 함수 추가
from schemas import CustomInterestResponse, GroupInterestsRequest
import crud
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from auth_utils import create_access_token, verify_password  # ✅ JWT 유틸리티 함수
from sqlalchemy import func
import schemas  # ✅ 사용자 스키마 사용을 위해 추가
from fastapi.responses import StreamingResponse
import io
import csv
from pydantic import BaseModel

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# ✅ 수정됨: user.is_admin → admin is None 체크 방식으로 변경
def check_admin(admin: Admin):
    # 🔧 기존 코드: if not user.is_admin: → 잘못된 참조
    # ✅ 수정 코드:
    if admin is None:
        raise HTTPException(status_code=401, detail="관리자 인증 실패")

# ✅ 1. 업체 등록 승인 API
@router.put("/providers/{provider_id}/approve")
def approve_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="업체를 찾을 수 없습니다.")

    provider.is_approved = True
    db.commit()
    return {"message": f"업체 '{provider.name}'가 승인되었습니다."}

# ✅ 2. 사용자 목록 조회
@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    users = db.query(User).all()
    return users

# ✅ 3. 사용자 삭제
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    db.delete(user)
    db.commit()
    return {"message": f"사용자 '{user.name}' 삭제 완료."}

# ✅ 4. 관리자 대시보드 통계
@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    return {
        "total_users": db.query(User).count(),
        "total_providers": db.query(Provider).count(),
        "total_activities": db.query(Activity).count()
    }

# ✅ 5. 사용자 주관식 관심사 전체 조회
@router.get("/custom-interests", response_model=List[CustomInterestResponse])
def read_custom_interests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return crud.get_all_custom_interests(db)

# ✅ 6. 주관식 관심사 통합 및 승인
@router.post("/group-interests", response_model=List[CustomInterestResponse])
def group_and_approve_custom_interests(
    request: GroupInterestsRequest,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    updated = crud.group_and_approve_interests(
        db,
        interest_ids=request.interest_ids,
        group_id=request.group_id
    )
    if not updated:
        raise HTTPException(status_code=404, detail="선택한 항목이 없습니다.")
    return updated

# ✅ 7. 관리자 로그인 (토큰 발급)
@router.post("/login")
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.email == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    token = create_access_token(data={"sub": str(admin.id)})
    return {"access_token": token, "token_type": "bearer"}

# ✅ 8. 관심사 그룹별 통계
@router.get("/stats/interests")
def get_interest_group_stats(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    results = (
        db.query(CustomInterest.group_id, func.count(CustomInterest.id))
        .filter(CustomInterest.status == "approved")
        .group_by(CustomInterest.group_id)
        .all()
    )

    response = []
    for group_id, count in results:
        group_name = f"그룹 {group_id}" if group_id else "미분류"
        response.append({
            "group_id": group_id,
            "group_name": group_name,
            "count": count
        })
    return response

# ✅ 9. 지역별 관심사 통계
@router.get("/stats/regions")
def get_region_interest_stats(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    results = (
        db.query(Activity.region, Activity.interest_subcategory, func.count(Activity.id))
        .group_by(Activity.region, Activity.interest_subcategory)
        .all()
    )

    region_stats = {}
    for region, interest, count in results:
        if region not in region_stats:
            region_stats[region] = []
        region_stats[region].append({"interest": interest, "count": count})

    return region_stats

# ✅ 관리자 대시보드 요약 통계 API
@router.get("/stats/summary")
def get_summary_stats(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    total_users = db.query(User).count()
    total_providers = db.query(Provider).count()
    total_admins = db.query(Admin).count()

    return {
        "total_users": total_users,
        "total_providers": total_providers,
        "total_admins": total_admins
    }


# 👇 맨 아래에 추가
@router.get("/providers", response_model=List[schemas.ProviderOut])
def get_all_providers(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    check_admin(current_admin)

    providers = db.query(Provider).all()
    return providers

@router.patch("/providers/{provider_id}/approve", response_model=schemas.ProviderOut)
def approve_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="업체를 찾을 수 없습니다.")

    provider.is_approved = True
    db.commit()
    db.refresh(provider)

    # ✅ 승인 알림 전송
    notification = Notification(
        provider_id=provider.id,
        message="업체 승인이 완료되었습니다.",
        is_read=False
    )
    db.add(notification)
    db.commit()

    return provider

@router.patch("/providers/{provider_id}/approve")
def approve_provider(provider_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)):
    """
    업체 승인 처리 API
    """
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="해당 업체를 찾을 수 없습니다.")

    # ✅ 승인 상태 변경
    provider.is_approved = True
    db.commit()
    db.refresh(provider)

    return {"message": f"{provider.name} 업체가 승인되었습니다."}

@router.get("/stats/users-by-region")
def get_users_by_region(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    result = (
    db.query(
        User.location,
        func.count(User.id).label("count")
    )
    .group_by(User.location)
    .all()
    )

    return [
       {
        "region": row.location,
        "count": row.count
       }
       for row in result
    ]


# routers/admin.py 맨 아래쪽에 추가하면 좋아요
@router.delete("/custom-interests/{id}", status_code=204)
def delete_custom_interest(
    id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)
    interest = db.query(CustomInterest).filter(CustomInterest.id == id).first()
    if not interest:
        raise HTTPException(status_code=404, detail="해당 관심사를 찾을 수 없습니다.")
    db.delete(interest)
    db.commit()
    return

@router.post("/interests", response_model=schemas.InterestOut)
def create_official_interest(
    interest_data: schemas.InterestCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    new_interest = Interest(
        category=interest_data.category,
        subcategory=interest_data.subcategory
    )
    db.add(new_interest)
    db.commit()
    db.refresh(new_interest)

    return schemas.InterestOut.from_orm(new_interest)  # ✅ SQLAlchemy 객체 → Pydantic 모델로 변환

# ✅ 사용자 전체 CSV 다운로드 API
@router.get("/users/download")
def download_users_csv(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)  # 관리자 권한 확인

    users = db.query(User).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "email", "phone", "location", "interests"])

    for user in users:
        writer.writerow([
            user.id,
            user.name,
            user.email,
            user.phone,
            user.location,
            user.interests
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=users.csv"
    })


# ✅ 업체 전체 CSV 다운로드 API
@router.get("/providers/download")
def download_providers_csv(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    providers = db.query(Provider).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "name", "email", "phone", "service_area",
        "service_name", "is_business", "business_registration_number", "is_approved"
    ])

    for p in providers:
        writer.writerow([
            p.id,
            p.name,
            p.email,
            p.phone,
            p.service_area,
            p.service_name,
            p.is_business,
            p.business_registration_number,
            p.is_approved
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=providers.csv"
    })

@router.get("/stats/registrations-by-date")
def get_registrations_by_date(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    user_data = (
        db.query(func.date(User.created_at).label("date"), func.count(User.id).label("user_count"))
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
        .all()
    )

    provider_data = (
        db.query(func.date(Provider.created_at).label("date"), func.count(Provider.id).label("provider_count"))
        .group_by(func.date(Provider.created_at))
        .order_by(func.date(Provider.created_at))
        .all()
    )

    # 날짜 기준 병합
    summary = {}
    for row in user_data:
        summary[str(row.date)] = {"date": str(row.date), "user_count": row.user_count, "provider_count": 0}
    for row in provider_data:
        date_str = str(row.date)
        if date_str not in summary:
            summary[date_str] = {"date": date_str, "user_count": 0, "provider_count": row.provider_count}
        else:
            summary[date_str]["provider_count"] = row.provider_count

    return list(summary.values())

# admin.py 하단 또는 기존 승인 관련 API 위
@router.get("/pending-providers", response_model=List[schemas.ProviderPendingResponse])
def get_pending_providers(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    pending = db.query(Provider).filter(Provider.is_approved == False).order_by(Provider.created_at.desc()).all()
    return pending

# ✅ 거절 요청용 스키마
class ProviderRejectionRequest(BaseModel):
    reason: str

@router.post("/providers/{provider_id}/reject")
def reject_provider(
    provider_id: int,
    request: ProviderRejectionRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="업체를 찾을 수 없습니다.")  # ✅ 여기!

    notification = Notification(
        provider_id=provider.id,
        message=f"업체 등록이 거절되었습니다. 사유: {request.reason}",
        is_read=False
    )
    db.add(notification)
    db.commit()

    return {"message": "거절 알림이 전송되었습니다."}

@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
    search: str = Query("", description="검색어"),
    sort: str = Query("created_at", description="정렬 기준 (created_at, name, email)"),
    order: str = Query("desc", description="정렬 방향 (asc, desc)")
):
    check_admin(current_admin)
    return crud.get_users_with_filters(db, search=search, sort=sort, order=order)


@router.get("/providers", response_model=List[schemas.ProviderOut])
def get_all_providers(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
    search: str = Query("", description="검색어"),
    sort: str = Query("created_at", description="정렬 기준 (created_at, name, email)"),
    order: str = Query("desc", description="정렬 방향 (asc, desc)")
):
    check_admin(current_admin)
    return crud.get_providers_with_filters(db, search=search, sort=sort, order=order)
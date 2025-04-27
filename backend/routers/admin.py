from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.models import User, Provider, Activity, CustomInterest, Admin, Interest, Notification
from auth_utils import get_current_admin
from schemas import (
    CustomInterestResponse, GroupInterestsRequest,
    UserResponse, ProviderOut, ProviderPendingResponse,
    InterestOut, InterestCreate
)
import crud
from fastapi.responses import StreamingResponse
import io
import csv
from sqlalchemy import func
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])

# ✅ 관리자 승인 확인
def check_admin(admin: Admin):
    if admin is None:
        raise HTTPException(status_code=401, detail="관리자 인증 실패")

# ✅ 1. 업체 등록 승인 API
@router.patch("/providers/{provider_id}/approve", response_model=ProviderOut)
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

    notification = Notification(
        provider_id=provider.id,
        message="업체 승인이 완료되었습니다.",
        is_read=False
    )
    db.add(notification)
    db.commit()

    return provider

# ✅ 2. 승인 대기 업체 조회
@router.get("/pending-providers", response_model=list[ProviderPendingResponse])
def get_pending_providers(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)
    pending = db.query(Provider).filter(Provider.is_approved == False).order_by(Provider.created_at.desc()).all()
    return pending

# ✅ 3. 사용자 전체 조회 (검색/정렬 지원)
@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
    search: str = Query("", description="검색어"),
    sort: str = Query("created_at", description="정렬 기준"),
    order: str = Query("desc", description="정렬 방향")
):
    check_admin(current_admin)
    return crud.get_users_with_filters(db, search=search, sort=sort, order=order)

# ✅ 4. 공급자 전체 조회 (검색/정렬 지원)
@router.get("/providers", response_model=list[ProviderOut])
def get_all_providers(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
    search: str = Query("", description="검색어"),
    sort: str = Query("created_at", description="정렬 기준"),
    order: str = Query("desc", description="정렬 방향")
):
    check_admin(current_admin)
    return crud.get_providers_with_filters(db, search=search, sort=sort, order=order)

# ✅ 5. 사용자 삭제
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    db.delete(user)
    db.commit()
    return {"message": f"사용자 '{user.name}' 삭제 완료."}

# ✅ 6. 관리자 대시보드 요약 통계
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

# ✅ 7. 사용자 CSV 다운로드
@router.get("/users/download")
def download_users_csv(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)

    users = db.query(User).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "email", "phone", "location", "interests"])

    for user in users:
        writer.writerow([
            user.id, user.name, user.email, user.phone, user.location, user.interests
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=users.csv"
    })

# ✅ 8. 업체 CSV 다운로드
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
            p.id, p.name, p.email, p.phone, p.service_area,
            p.service_name, p.is_business, p.business_registration_number, p.is_approved
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=providers.csv"
    })

# ✅ 9. 사용자 지역별 통계
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

# ✅ 10. 주관식 관심사 전체 조회
@router.get("/custom-interests", response_model=list[CustomInterestResponse])
def read_custom_interests(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)
    return crud.get_all_custom_interests(db)

# ✅ 11. 주관식 관심사 통합 및 승인
@router.post("/group-interests", response_model=list[CustomInterestResponse])
def group_and_approve_custom_interests(
    request: GroupInterestsRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    check_admin(current_admin)
    updated = crud.group_and_approve_interests(
        db,
        interest_ids=request.interest_ids,
        group_id=request.group_id
    )
    if not updated:
        raise HTTPException(status_code=404, detail="선택한 항목이 없습니다.")
    return updated

# ✅ 12. 주관식 관심사 삭제
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

# ✅ 13. 공식 관심사 추가
@router.post("/interests", response_model=InterestOut)
def create_official_interest(
    interest_data: InterestCreate,
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

    return InterestOut.from_orm(new_interest)

# ✅ 14. 날짜별 사용자/업체 가입 통계
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

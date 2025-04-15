from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import Payment, Activity
from schemas import PaymentCreate, PaymentResponse
from auth_utils import get_current_user  # ✅ JWT에서 사용자 정보 가져오기
import datetime

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

# ✅ 결제 생성 API (JWT에서 user_id 가져오기)
@router.post("/", response_model=PaymentResponse)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    activity = db.query(Activity).filter(Activity.id == payment_data.activity_id).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    new_payment = Payment(
        user_id=user.id,  # ✅ JWT에서 가져온 현재 로그인된 사용자 ID 사용
        activity_id=payment_data.activity_id,
        amount=payment_data.amount,
        status="pending",
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

# ✅ 특정 결제 조회 API
@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# ✅ 내 결제 목록 조회 API (JWT 적용)
@router.get("/", response_model=list[PaymentResponse])
def get_user_payments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    payments = db.query(Payment).filter(Payment.user_id == user.id).all()
    return payments

# ✅ 결제 완료 API
@router.put("/{payment_id}/complete", response_model=PaymentResponse)
def complete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.status != "pending":
        raise HTTPException(status_code=400, detail="Payment cannot be completed")
    
    payment.status = "completed"
    db.commit()
    db.refresh(payment)
    return payment

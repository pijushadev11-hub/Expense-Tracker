from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional
from ..database import get_db
from ..models.transaction import TransactionType
from ..services.transaction_service import TransactionService
from ..auth.jwt_handler import verify_token

router = APIRouter(prefix="/transactions", tags=["transactions"])

class TransactionCreate(BaseModel):
    type: TransactionType
    amount: float
    category: str
    description: Optional[str] = None
    date: date

class TransactionResponse(BaseModel):
    id: int
    type: TransactionType
    amount: float
    category: str
    description: Optional[str]
    date: date

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    return verify_token(token)

@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return TransactionService.create_transaction(
        db, user_id, transaction.dict()
    )

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return TransactionService.get_user_transactions(db, user_id)

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    now = datetime.now()
    return TransactionService.get_dashboard_data(
        db, user_id, now.year, now.month
    )
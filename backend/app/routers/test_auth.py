from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..auth.jwt_handler import create_access_token

router = APIRouter(prefix="/test", tags=["test"])

@router.post("/login")
def test_login(db: Session = Depends(get_db)):
    # Create or get test user
    user = db.query(User).filter(User.email == "test@example.com").first()
    if not user:
        user = User(
            email="test@example.com",
            name="Test User",
            provider="test"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    access_token = create_access_token({"user_id": user.id})
    return {
        "access_token": access_token, 
        "user": {"id": user.id, "email": user.email, "name": user.name}
    }
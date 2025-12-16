from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models.user import User
from ..auth.jwt_handler import create_access_token
from ..auth.oauth import oauth, get_user_info

router = APIRouter(prefix="/auth", tags=["authentication"])

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

@router.get("/google")
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await get_user_info('google', token)
    
    user = db.query(User).filter(User.email == user_info['email']).first()
    if not user:
        user = User(
            email=user_info['email'],
            name=user_info['name'],
            provider='google',
            provider_id=user_info['provider_id']
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    access_token = create_access_token({"user_id": user.id})
    return {"access_token": access_token, "user": UserResponse.from_orm(user)}

@router.get("/apple")
async def apple_login(request: Request):
    redirect_uri = request.url_for('apple_callback')
    return await oauth.apple.authorize_redirect(request, redirect_uri)

@router.get("/apple/callback")
async def apple_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.apple.authorize_access_token(request)
    user_info = await get_user_info('apple', token)
    
    user = db.query(User).filter(User.email == user_info['email']).first()
    if not user:
        user = User(
            email=user_info['email'],
            name=user_info['name'],
            provider='apple',
            provider_id=user_info['provider_id']
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    access_token = create_access_token({"user_id": user.id})
    return {"access_token": access_token, "user": UserResponse.from_orm(user)}
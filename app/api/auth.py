# app/api/auth.py
"""
Defines authentication endpoints for registering and logging in users.
Delegates logic to the auth service layer.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth_schemas import UserRegister, UserLogin
from app.services.auth_service import register_user, login_user
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(payload, db)

@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return login_user(payload, db)

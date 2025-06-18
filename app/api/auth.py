# app/api/auth.py
"""
Defines authentication endpoints for registering and logging in users.
Delegates logic to the auth service layer.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth_schemas import UserRegister, UserLogin
from app.services.auth_service import register_user, login_user

router = APIRouter()

@router.post("/register")
def register(payload: UserRegister):
    return register_user(payload)

@router.post("/login")
def login(payload: UserLogin):
    return login_user(payload)

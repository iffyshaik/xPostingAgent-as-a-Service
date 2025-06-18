# app/schemas/auth_schemas.py
"""
Pydantic models for validating user input during registration and login.
"""

from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

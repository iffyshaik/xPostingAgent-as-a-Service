# app/utils/security.py

import bcrypt

def hash_password(plain_password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    """
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed bcrypt password.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

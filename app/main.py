# app/main.py
"""
Entrypoint for the FastAPI application.
This initialises the app and includes routes such as authentication.
"""

from fastapi import FastAPI
from app.api import auth

app = FastAPI(
    title="Social Media Posting Agent API",
    version="0.1.0",
    description="Handles user authentication and future agent interactions."
)

# Include the authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.service.user_service import UserService
from app.entities.user import (
    UserCreate, 
    UserLogin, 
    UserResponse, 
    Token, 
    ForgotPassword, 
    PasswordReset
)
from app.core.deps import get_current_active_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register new user.
    """
    user_service = UserService(db)
    return user_service.register_user(user_create)


@router.post("/login", response_model=Token)
def login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    Login user and return access token.
    """
    user_service = UserService(db)
    return user_service.authenticate_user(user_login)


@router.post("/forgot-password", response_model=dict)
def forgot_password(
    forgot_password: ForgotPassword,
    db: Session = Depends(get_db)
) -> Any:
    """
    Send password reset email.
    """
    user_service = UserService(db)
    return user_service.forgot_password(forgot_password)


@router.post("/reset-password", response_model=dict)
def reset_password(
    password_reset: PasswordReset,
    db: Session = Depends(get_db)
) -> Any:
    """
    Reset password using token.
    """
    user_service = UserService(db)
    return user_service.reset_password(password_reset)


@router.get("/verify-email", response_model=dict)
def verify_email(
    token: str = Query(...),
    db: Session = Depends(get_db)
) -> Any:
    """
    Verify user email using token.
    """
    user_service = UserService(db)
    return user_service.verify_email(token)


@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: UserResponse = Depends(get_current_active_user)
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/logout", response_model=dict)
def logout() -> Any:
    """
    Logout user (token invalidation should be handled on client side).
    """
    return {"message": "Successfully logged out"}
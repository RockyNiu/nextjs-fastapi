from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.db.service.user_service import UserService
from app.entities.user import UserCreate, UserLogin, User, Token, ForgotPassword, PasswordReset
from app.api.entities.user_api import (
    UserCreateAPI,
    UserLoginAPI, 
    UserAPI,
    TokenResponseAPI,
    ForgotPasswordAPI,
    PasswordResetAPI,
    MessageResponseAPI,
    ErrorResponseAPI
)
from app.core.deps import get_current_active_user

router = APIRouter()


@router.post("/register", response_model=UserAPI)
def register(
    user_create_api: UserCreateAPI
) -> Any:
    """
    Register new user.
    """
    # Convert API model to internal model
    user_create = UserCreate(
        email=user_create_api.email,
        first_name=user_create_api.first_name,
        last_name=user_create_api.last_name,
        password=user_create_api.password
    )
    
    user_service = UserService()
    user = user_service.register_user(user_create)
    
    # Convert internal model to API response model
    return UserAPI.model_validate(user)


@router.post("/login", response_model=TokenResponseAPI)
def login(
    user_login_api: UserLoginAPI
) -> Any:
    """
    Login user and return access token.
    """
    # Convert API model to internal model
    user_login = UserLogin(
        email=user_login_api.email,
        password=user_login_api.password
    )
    
    user_service = UserService()
    token = user_service.authenticate_user(user_login)
    
    # Convert internal model to API response model
    return TokenResponseAPI(
        access_token=token.access_token,
        token_type=token.token_type,
        expires_in=token.expires_in
    )


@router.post("/forgot-password", response_model=MessageResponseAPI)
def forgot_password(
    forgot_password_api: ForgotPasswordAPI
) -> Any:
    """
    Send password reset email.
    """
    # Convert API model to internal model
    forgot_password = ForgotPassword(email=forgot_password_api.email)
    
    user_service = UserService()
    result = user_service.forgot_password(forgot_password)
    
    # Convert dict response to API response model
    return MessageResponseAPI(message=result.get("message", "Password reset email sent"))


@router.post("/reset-password", response_model=MessageResponseAPI)
def reset_password(
    password_reset_api: PasswordResetAPI
) -> Any:
    """
    Reset password using token.
    """
    # Convert API model to internal model
    password_reset = PasswordReset(
        token=password_reset_api.token,
        new_password=password_reset_api.new_password
    )
    
    user_service = UserService()
    result = user_service.reset_password(password_reset)
    
    # Convert dict response to API response model
    return MessageResponseAPI(message=result.get("message", "Password reset successfully"))


@router.get("/verify-email", response_model=MessageResponseAPI)
def verify_email(
    token: str = Query(...)
) -> Any:
    """
    Verify user email using token.
    """
    user_service = UserService()
    result = user_service.verify_email(token)
    
    # Convert dict response to API response model
    return MessageResponseAPI(message=result.get("message", "Email verified successfully"))


@router.get("/me", response_model=UserAPI)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user.
    """
    # Convert internal model to API response model
    return UserAPI.model_validate(current_user)


@router.post("/logout", response_model=MessageResponseAPI)
def logout() -> Any:
    """
    Logout user (token invalidation should be handled on client side).
    """
    return MessageResponseAPI(message="Successfully logged out")
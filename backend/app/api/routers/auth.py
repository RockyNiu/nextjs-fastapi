from typing import Any

from fastapi import APIRouter, Depends, Query, status

from app.api.entities.user_api import (
    ErrorResponseAPI,
    ForgotPasswordAPI,
    MessageResponseAPI,
    PasswordResetAPI,
    TokenResponseAPI,
    UserAPI,
    UserCreateAPI,
    UserLoginAPI,
)
from app.core.deps import get_current_active_user
from app.entities.user import (
    ForgotPassword,
    PasswordReset,
    User,
    UserCreate,
    UserLogin,
)
from app.service.user_service import UserService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserAPI,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User successfully registered"},
        400: {
            "model": ErrorResponseAPI,
            "description": "Bad request - validation error",
        },
        409: {
            "model": ErrorResponseAPI,
            "description": "Conflict - user already exists",
        },
    },
    summary="Register new user",
    description="Register a new user with email, first name, last name, and password.",
)
def register(user_create_api: UserCreateAPI) -> Any:
    """
    Register new user.
    """
    # Convert API model to internal model
    user_create = UserCreate(
        email=user_create_api.email,
        first_name=user_create_api.first_name,
        last_name=user_create_api.last_name,
        password=user_create_api.password,
    )

    user_service = UserService()
    user = user_service.register_user(user_create)

    return UserAPI.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponseAPI,
    responses={
        200: {"description": "Login successful - returns access token"},
        400: {
            "model": ErrorResponseAPI,
            "description": "Bad request - invalid credentials",
        },
        401: {
            "model": ErrorResponseAPI,
            "description": "Unauthorized - authentication failed",
        },
    },
    summary="User login",
    description="Authenticate user and return JWT access token.",
)
def login(user_login_api: UserLoginAPI) -> Any:
    """
    Login user and return access token.
    """
    # Convert API model to internal model
    user_login = UserLogin(email=user_login_api.email, password=user_login_api.password)

    user_service = UserService()
    token = user_service.authenticate_user(user_login)

    # Convert internal model to API response model
    return TokenResponseAPI(
        access_token=token.access_token,
        token_type=token.token_type,
        expires_in=token.expires_in,
    )


@router.post(
    "/forgot-password",
    response_model=MessageResponseAPI,
    responses={
        200: {"description": "Password reset email sent"},
        400: {"model": ErrorResponseAPI, "description": "Bad request - invalid email"},
        404: {"model": ErrorResponseAPI, "description": "User not found"},
    },
    summary="Request password reset",
    description="Send password reset email to user.",
)
def forgot_password(forgot_password_api: ForgotPasswordAPI) -> Any:
    """
    Send password reset email.
    """
    # Convert API model to internal model
    forgot_password = ForgotPassword(email=forgot_password_api.email)

    user_service = UserService()
    result = user_service.forgot_password(forgot_password)

    # Convert dict response to API response model
    return MessageResponseAPI(
        message=result.get("message", "Password reset email sent"), success=True
    )


@router.post(
    "/reset-password",
    response_model=MessageResponseAPI,
    responses={
        200: {"description": "Password reset successful"},
        400: {
            "model": ErrorResponseAPI,
            "description": "Bad request - invalid token or password",
        },
        404: {"model": ErrorResponseAPI, "description": "Invalid or expired token"},
    },
    summary="Reset password",
    description="Reset user password using reset token.",
)
def reset_password(password_reset_api: PasswordResetAPI) -> Any:
    """
    Reset password using token.
    """
    # Convert API model to internal model
    password_reset = PasswordReset(
        token=password_reset_api.token, new_password=password_reset_api.new_password
    )

    user_service = UserService()
    result = user_service.reset_password(password_reset)

    # Convert dict response to API response model
    return MessageResponseAPI(
        message=result.get("message", "Password reset successfully"), success=True
    )


@router.get(
    "/verify-email",
    response_model=MessageResponseAPI,
    responses={
        200: {"description": "Email verified successfully"},
        400: {"model": ErrorResponseAPI, "description": "Bad request - invalid token"},
        404: {"model": ErrorResponseAPI, "description": "Invalid or expired token"},
    },
    summary="Verify email address",
    description="Verify user email address using verification token.",
)
def verify_email(
    token: str = Query(..., description="Email verification token"),
) -> Any:
    """
    Verify user email using token.
    """
    user_service = UserService()
    result = user_service.verify_email(token)

    # Convert dict response to API response model
    return MessageResponseAPI(
        message=result.get("message", "Email verified successfully"), success=True
    )


@router.get(
    "/me",
    response_model=UserAPI,
    responses={
        200: {"description": "Current user information"},
        401: {
            "model": ErrorResponseAPI,
            "description": "Unauthorized - invalid or expired token",
        },
    },
    summary="Get current user",
    description="Get current authenticated user information.",
)
def read_user_me(current_user: User = Depends(get_current_active_user)) -> Any:
    """
    Get current user.
    """
    # Convert internal model to API response model
    return UserAPI.model_validate(current_user)


@router.post(
    "/logout",
    response_model=MessageResponseAPI,
    responses={
        200: {"description": "Successfully logged out"},
    },
    summary="User logout",
    description="Logout user (token invalidation should be handled on client side).",
)
def logout() -> Any:
    """
    Logout user (token invalidation should be handled on client side).
    """
    return MessageResponseAPI(message="Successfully logged out", success=True)

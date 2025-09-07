from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.entities.user_api import (
    EmailVerificationResponseAPI,
    ErrorResponseAPI,
    ForgotPasswordAPI,
    MessageResponseAPI,
    PasswordResetAPI,
    TokenResponseAPI,
    UserAPI,
    UserCreateAPI,
    UserLoginAPI,
    UserRegistrationResponseAPI,
)
from app.core.deps import get_current_active_user
from app.entities.user import (
    ForgotPassword,
    PasswordReset,
    User,
    UserCreate,
    UserLogin,
)
from app.exceptions.user_exceptions import (
    EmailAlreadyVerifiedError,
    EmailSendError,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidPasswordResetTokenError,
    InvalidVerificationTokenError,
    NoVerificationTokenError,
    UserAlreadyExistsError,
)
from app.service.user_service import UserService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRegistrationResponseAPI,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User successfully registered with authentication token"},
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
    description="Register a new user with email, first name, last name, and password. Returns user data and authentication token for automatic login.",
)
async def register(user_create_api: UserCreateAPI) -> Any:
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

    try:
        result = await user_service.register_user(user_create)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    return UserRegistrationResponseAPI(
        user=UserAPI.model_validate(result.user),
        access_token=result.token.access_token,
        token_type=result.token.token_type,
        expires_in=result.token.expires_in,
    )


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

    try:
        token = user_service.authenticate_user(user_login)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InactiveUserError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is inactive",
        )

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
async def forgot_password(forgot_password_api: ForgotPasswordAPI) -> Any:
    """
    Send password reset email.
    """
    # Convert API model to internal model
    forgot_password = ForgotPassword(email=forgot_password_api.email)

    user_service = UserService()
    await user_service.forgot_password(forgot_password)

    return MessageResponseAPI(
        message="If the email exists, a password reset link has been sent", success=True
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

    try:
        user_service.reset_password(password_reset)
    except InvalidPasswordResetTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    return MessageResponseAPI(message="Password reset successfully", success=True)


@router.get(
    "/verify-email",
    response_model=EmailVerificationResponseAPI,
    responses={
        200: {"description": "Email verified successfully with authentication token"},
        400: {"model": ErrorResponseAPI, "description": "Bad request - invalid token"},
        404: {"model": ErrorResponseAPI, "description": "Invalid or expired token"},
    },
    summary="Verify email address",
    description="Verify user email address using verification token and return authentication token for automatic login.",
)
def verify_email(
    token: str = Query(..., description="Email verification token"),
) -> Any:
    """
    Verify user email using token and return authentication token.
    """
    user_service = UserService()

    try:
        result = user_service.verify_email(token)
    except InvalidVerificationTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token. If you recently verified your email, please log in to your account.",
        )

    # Convert response to API response model
    return EmailVerificationResponseAPI(
        message="Email verified successfully",
        success=True,
        access_token=result.token.access_token,
        token_type=result.token.token_type,
        expires_in=result.token.expires_in,
    )


@router.post(
    "/resend-verification",
    response_model=MessageResponseAPI,
    responses={
        200: {"description": "Verification email sent successfully"},
        400: {
            "model": ErrorResponseAPI,
            "description": "Bad request - email already verified or no token found",
        },
        401: {
            "model": ErrorResponseAPI,
            "description": "Unauthorized - invalid or expired token",
        },
        500: {
            "model": ErrorResponseAPI,
            "description": "Internal server error - failed to send email",
        },
    },
    summary="Resend verification email",
    description="Resend email verification for the current authenticated user.",
)
async def resend_verification_email(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Resend verification email to current user.
    """
    user_service = UserService()

    try:
        await user_service.resend_verification_email(current_user)
    except EmailAlreadyVerifiedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified",
        )
    except NoVerificationTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No verification token found",
        )
    except EmailSendError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email",
        )

    return MessageResponseAPI(
        message="Verification email sent successfully", success=True
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

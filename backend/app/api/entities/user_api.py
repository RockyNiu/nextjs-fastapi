from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreateAPI(BaseModel):
    """API model for user creation requests from frontend"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)


class UserLoginAPI(BaseModel):
    """API model for user login requests from frontend"""
    email: EmailStr
    password: str


class UserAPI(BaseModel):
    """API model for user data responses to frontend"""
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    date_created: datetime
    date_updated: datetime
    email_verified: bool

    class Config:
        from_attributes = True


class TokenResponseAPI(BaseModel):
    """API model for authentication token responses to frontend"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class ForgotPasswordAPI(BaseModel):
    """API model for forgot password requests from frontend"""
    email: EmailStr


class PasswordResetAPI(BaseModel):
    """API model for password reset requests from frontend"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class MessageResponseAPI(BaseModel):
    """API model for simple message responses to frontend"""
    message: str
    success: bool = True


class ErrorResponseAPI(BaseModel):
    """API model for error responses to frontend"""
    error: str
    detail: Optional[str] = None
    success: bool = False
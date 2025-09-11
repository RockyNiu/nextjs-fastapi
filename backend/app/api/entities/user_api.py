from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.db.orm.user_role_orm import UserRole


class UserCreateAPI(BaseModel):
    """API model for user creation requests from frontend"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword123",
            }
        }
    )

    email: Annotated[
        EmailStr,
        Field(
            description="User's email address",
            json_schema_extra={"example": "user@example.com"},
        ),
    ]
    first_name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="User's first name",
            json_schema_extra={"example": "John"},
        ),
    ]
    last_name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="User's last name",
            json_schema_extra={"example": "Doe"},
        ),
    ]
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
            description="User's password (minimum 8 characters)",
            json_schema_extra={"example": "securepassword123"},
        ),
    ]


class UserLoginAPI(BaseModel):
    """API model for user login requests from frontend"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "user@example.com", "password": "securepassword123"}
        }
    )

    email: Annotated[
        EmailStr,
        Field(
            description="User's email address",
            json_schema_extra={"example": "user@example.com"},
        ),
    ]
    password: Annotated[
        str,
        Field(
            description="User's password",
            json_schema_extra={"example": "securepassword123"},
        ),
    ]


class UserAPI(BaseModel):
    """API model for user data responses to frontend"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
                "date_created": "2025-01-01T12:00:00Z",
                "date_updated": "2025-01-01T12:00:00Z",
                "email_verified": True,
            }
        },
    )

    id: Annotated[
        int,
        Field(description="User's unique identifier", json_schema_extra={"example": 1}),
    ]
    email: Annotated[
        str,
        Field(
            description="User's email address",
            json_schema_extra={"example": "user@example.com"},
        ),
    ]
    first_name: Annotated[
        str,
        Field(description="User's first name", json_schema_extra={"example": "John"}),
    ]
    last_name: Annotated[
        str, Field(description="User's last name", json_schema_extra={"example": "Doe"})
    ]
    is_active: Annotated[
        bool,
        Field(
            description="Whether the user account is active",
            json_schema_extra={"example": True},
        ),
    ]
    date_created: Annotated[
        datetime,
        Field(
            description="User account creation timestamp",
            json_schema_extra={"example": "2025-01-01T12:00:00Z"},
        ),
    ]
    date_updated: Annotated[
        datetime,
        Field(
            description="User account last update timestamp",
            json_schema_extra={"example": "2025-01-01T12:00:00Z"},
        ),
    ]
    email_verified: Annotated[
        bool,
        Field(
            description="Whether the user's email is verified",
            json_schema_extra={"example": True},
        ),
    ]
    role_id: Annotated[
        UserRole,
        Field(
            description="User's role ID",
            json_schema_extra={"example": UserRole.USER},
        ),
    ]


class UserUpdateAPI(BaseModel):
    """API model for user update requests from frontend"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
                "role_id": UserRole.USER,
            }
        }
    )

    first_name: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=100,
            description="User's first name",
            json_schema_extra={"example": "John"},
        ),
    ]
    last_name: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=100,
            description="User's last name",
            json_schema_extra={"example": "Doe"},
        ),
    ]
    is_active: Annotated[
        Optional[bool],
        Field(
            default=None,
            description="Whether the user account is active",
            json_schema_extra={"example": True},
        ),
    ]
    role_id: Annotated[
        Optional[UserRole],
        Field(
            default=None,
            description="User's role ID",
            json_schema_extra={"example": UserRole.USER},
        ),
    ]


class UserListResponseAPI(BaseModel):
    """API model for user list responses to frontend"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "users": [
                    {
                        "id": 1,
                        "email": "user1@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_active": True,
                        "role_id": UserRole.USER,
                        "date_created": "2025-01-01T12:00:00Z",
                        "date_updated": "2025-01-01T12:00:00Z",
                        "email_verified": True,
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 100,
            }
        }
    )

    users: Annotated[
        List[UserAPI],
        Field(description="List of users"),
    ]
    total: Annotated[
        int,
        Field(
            description="Total number of users returned",
            json_schema_extra={"example": 1},
        ),
    ]
    skip: Annotated[
        int,
        Field(description="Number of users skipped", json_schema_extra={"example": 0}),
    ]
    limit: Annotated[
        int,
        Field(
            description="Maximum number of users returned",
            json_schema_extra={"example": 100},
        ),
    ]


class TokenAPI(BaseModel):
    """API model for authentication token data"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
            }
        }
    )

    access_token: Annotated[
        str,
        Field(
            description="JWT access token",
            json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
        ),
    ]
    token_type: Annotated[
        str,
        Field(
            default="bearer",
            description="Token type",
            json_schema_extra={"example": "bearer"},
        ),
    ]
    expires_in: Annotated[
        int,
        Field(
            description="Token expiration time in seconds",
            json_schema_extra={"example": 3600},
        ),
    ]


class TokenResponseAPI(TokenAPI):
    """API model for authentication token responses to frontend"""

    pass


class ForgotPasswordAPI(BaseModel):
    """API model for forgot password requests from frontend"""

    model_config = ConfigDict(
        json_schema_extra={"example": {"email": "user@example.com"}}
    )

    email: Annotated[
        EmailStr,
        Field(
            description="User's email address for password reset",
            json_schema_extra={"example": "user@example.com"},
        ),
    ]


class PasswordResetAPI(BaseModel):
    """API model for password reset requests from frontend"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "reset-token-123",
                "new_password": "newSecurePassword123",
            }
        }
    )

    token: Annotated[
        str,
        Field(
            description="Password reset token",
            json_schema_extra={"example": "reset-token-123"},
        ),
    ]
    new_password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
            description="New password (minimum 8 characters)",
            json_schema_extra={"example": "newSecurePassword123"},
        ),
    ]


class MessageResponseAPI(BaseModel):
    """API model for simple message responses to frontend"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"message": "Operation completed successfully", "success": True}
        }
    )

    message: Annotated[
        str,
        Field(
            description="Response message",
            json_schema_extra={"example": "Operation completed successfully"},
        ),
    ]
    success: Annotated[
        bool,
        Field(
            default=True,
            description="Whether the operation was successful",
            json_schema_extra={"example": True},
        ),
    ]


class EmailVerificationResponseAPI(TokenAPI):
    """API model for email verification responses that includes authentication token"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Email verified successfully",
                "success": True,
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
            }
        }
    )

    message: Annotated[
        str,
        Field(
            description="Verification message",
            json_schema_extra={"example": "Email verified successfully"},
        ),
    ]
    success: Annotated[
        bool,
        Field(
            default=True,
            description="Whether the verification was successful",
            json_schema_extra={"example": True},
        ),
    ]


class UserRegistrationResponseAPI(TokenAPI):
    """API model for user registration responses that includes user data and authentication token"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "firstName": "John",
                    "lastName": "Doe",
                    "isActive": True,
                    "emailVerified": False,
                    "dateCreated": "2025-01-01T12:00:00Z",
                    "dateUpdated": "2025-01-01T12:00:00Z",
                },
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
            }
        }
    )

    user: UserAPI


class ErrorResponseAPI(BaseModel):
    """API model for error responses to frontend"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "Validation Error",
                "detail": "Email already exists",
                "success": False,
            }
        }
    )

    error: Annotated[
        str,
        Field(
            description="Error message",
            json_schema_extra={"example": "Validation Error"},
        ),
    ]
    detail: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Detailed error information",
            json_schema_extra={"example": "Email already exists"},
        ),
    ]
    success: Annotated[
        bool,
        Field(
            default=False,
            description="Whether the operation was successful",
            json_schema_extra={"example": False},
        ),
    ]

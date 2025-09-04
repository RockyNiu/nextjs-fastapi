from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.dao.user_dao import UserDAO
from app.entities.user import UserCreate, UserLogin, UserResponse, Token, ForgotPassword, PasswordReset
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, generate_email_verification_token


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_dao = UserDAO(db)

    def register_user(self, user_create: UserCreate) -> UserResponse:
        # Check if user already exists
        if self.user_dao.get_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        db_user = self.user_dao.create_user(user_create)
        
        # Set email verification token
        db_user.email_verification_token = generate_email_verification_token()
        self.db.commit()
        
        # TODO: Send verification email here
        
        return UserResponse.model_validate(db_user)

    def authenticate_user(self, user_login: UserLogin) -> Token:
        user = self.user_dao.authenticate(user_login.email, user_login.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not self.user_dao.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
        )

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = self.user_dao.get_by_email(email)
        if user:
            return UserResponse.model_validate(user)
        return None

    def forgot_password(self, forgot_password: ForgotPassword) -> dict:
        user = self.user_dao.get_by_email(forgot_password.email)
        if not user:
            # Don't reveal if email exists or not
            return {"message": "If the email exists, a password reset link has been sent"}
        
        token = self.user_dao.set_password_reset_token(user)
        
        # TODO: Send password reset email here
        
        return {"message": "If the email exists, a password reset link has been sent"}

    def reset_password(self, password_reset: PasswordReset) -> dict:
        user = self.user_dao.reset_password_by_token(
            password_reset.token, 
            password_reset.new_password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        return {"message": "Password reset successfully"}

    def verify_email(self, token: str) -> dict:
        user = self.user_dao.verify_email(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token"
            )
        
        return {"message": "Email verified successfully"}
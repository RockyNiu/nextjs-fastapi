from datetime import timedelta
from typing import List, Optional

from app.common.logger import logger
from app.db.dao.user_dao import UserDAO
from app.entities.user import (
    ForgotPassword,
    PasswordReset,
    Token,
    User,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserWithAccessToken,
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
from app.service.auth_service import AuthService
from app.service.crypto_service import CryptoService
from app.service.email_service import EmailService


class UserService:
    def __init__(
        self,
        user_dao: Optional[UserDAO] = None,
        email_service: Optional[EmailService] = None,
        auth_service: Optional[AuthService] = None,
        crypto_service: Optional[CryptoService] = None,
    ):
        self.user_dao = user_dao or UserDAO()
        self.email_service = email_service or EmailService()
        self.auth_service = auth_service or AuthService()
        self.crypto_service = crypto_service or CryptoService()

    async def register_user(self, user_create: UserCreate) -> UserWithAccessToken:
        # Check if user already exists
        if self.user_dao.get_by_email(user_create.email):
            raise UserAlreadyExistsError("Email already registered")

        # Create user (email verification token is set in the DAO)
        db_user = self.user_dao.create_user(user_create)

        # Send verification email
        try:
            if db_user.email_verification_token:
                await self.email_service.send_verification_email(
                    db_user.email, db_user.email_verification_token
                )
        except Exception as e:
            logger.error(f"Failed to send verification email to {db_user.email}: {e}")
            raise EmailSendError("Failed to send verification email")

        # Generate access token for the new user
        user = User.model_validate(db_user)
        access_token_expires = timedelta(
            seconds=self.auth_service.ACCESS_TOKEN_EXPIRE_SECONDS
        )
        access_token = self.auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return UserWithAccessToken(
            user=user,
            token=Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=self.auth_service.ACCESS_TOKEN_EXPIRE_SECONDS,
            ),
        )

    def authenticate_user(self, user_login: UserLogin) -> Token:
        user = self.user_dao.authenticate(user_login.email, user_login.password)

        if not user:
            raise InvalidCredentialsError("Incorrect email or password")

        if not self.user_dao.is_active(user):
            raise InactiveUserError("User account is inactive")

        access_token_expires = timedelta(
            seconds=self.auth_service.ACCESS_TOKEN_EXPIRE_SECONDS
        )
        access_token = self.auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.auth_service.ACCESS_TOKEN_EXPIRE_SECONDS,
        )

    def get_user_by_email(self, email: str) -> Optional[User]:
        user = self.user_dao.get_by_email(email)
        if user:
            return User.model_validate(user)
        return None

    def get_user_by_token(self, token: str) -> Optional[User]:
        """Get user by JWT token"""
        email = self.auth_service.verify_token(token)
        if not email:
            return None

        return self.get_user_by_email(email)

    async def forgot_password(self, forgot_password: ForgotPassword) -> None:
        user = self.user_dao.get_by_email(forgot_password.email)
        if not user:
            return

        reset_token = self.user_dao.set_password_reset_token(forgot_password.email)

        try:
            await self.email_service.send_reset_password_email(
                forgot_password.email, reset_token
            )
        except Exception as e:
            # Log the error but don't reveal if email exists
            logger.error(
                f"Failed to send password reset email to {forgot_password.email}: {e}"
            )

    def reset_password(self, password_reset: PasswordReset) -> None:
        user = self.user_dao.reset_password_by_token(
            password_reset.token, password_reset.new_password
        )

        if not user:
            raise InvalidPasswordResetTokenError("Invalid or expired reset token")

    def verify_email(self, token: str) -> UserWithAccessToken:
        user = self.user_dao.verify_email(token)

        if not user:
            raise InvalidVerificationTokenError("Invalid or expired verification token")

        # Generate access token for the verified user
        access_token_expires = timedelta(
            seconds=self.auth_service.ACCESS_TOKEN_EXPIRE_SECONDS
        )
        access_token = self.auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return UserWithAccessToken(
            user=user,
            token=Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=self.auth_service.ACCESS_TOKEN_EXPIRE_SECONDS,
            ),
        )

    async def resend_verification_email(self, user: User) -> None:
        if user.email_verified:
            raise EmailAlreadyVerifiedError("Email is already verified")

        # Get the current user data with verification token
        db_user = self.user_dao.get_by_email(user.email)
        if not db_user or not db_user.email_verification_token:
            raise NoVerificationTokenError("No verification token found")

        # Send verification email
        try:
            await self.email_service.send_verification_email(
                db_user.email, db_user.email_verification_token
            )
        except Exception as e:
            logger.error(f"Failed to resend verification email to {db_user.email}: {e}")
            raise EmailSendError("Failed to send verification email")

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return self.user_dao.get_all_users(skip=skip, limit=limit)

    def get_total_users_count(self) -> int:
        """Get total count of all users."""
        return self.user_dao.count_all()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.user_dao.get_by_id(user_id)

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information."""
        return self.user_dao.update_user(user_id, user_update)

    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate a user account."""
        user_update = UserUpdate(is_active=False)
        return self.user_dao.update_user(user_id, user_update)

    def activate_user(self, user_id: int) -> Optional[User]:
        """Activate a user account."""
        user_update = UserUpdate(is_active=True)
        return self.user_dao.update_user(user_id, user_update)

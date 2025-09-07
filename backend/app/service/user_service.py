from datetime import timedelta
from typing import Optional

from app.core.logger import logger
from app.core.security import ACCESS_TOKEN_EXPIRE_SECONDS, create_access_token
from app.db.dao.user_dao import UserDAO
from app.entities.user import (
    ForgotPassword,
    PasswordReset,
    Token,
    User,
    UserCreate,
    UserLogin,
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
from app.service.email_service import EmailService


class UserService:
    def __init__(
        self,
        user_dao: Optional[UserDAO] = None,
        email_service: Optional[EmailService] = None,
    ):
        self.user_dao = user_dao or UserDAO()
        self.email_service = email_service or EmailService()

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
            # Log the error but don't fail registration
            logger.error(f"Failed to send verification email to {db_user.email}: {e}")

        # Generate access token for the new user
        user = User.model_validate(db_user)
        access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return UserWithAccessToken(
            user=user,
            token=Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
            ),
        )

    def authenticate_user(self, user_login: UserLogin) -> Token:
        user = self.user_dao.authenticate(user_login.email, user_login.password)

        if not user:
            raise InvalidCredentialsError("Incorrect email or password")

        if not self.user_dao.is_active(user):
            raise InactiveUserError("User account is inactive")

        access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
        )

    def get_user_by_email(self, email: str) -> Optional[User]:
        user = self.user_dao.get_by_email(email)
        if user:
            return User.model_validate(user)
        return None

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
        access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return UserWithAccessToken(
            user=user,
            token=Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
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

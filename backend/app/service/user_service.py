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
        """Get all users with pagination.

        Args:
            skip: Number of records to skip for pagination. Defaults to 0.
            limit: Maximum number of records to return. Defaults to 100.

        Returns:
            List of User objects.
        """
        return self.user_dao.get_all_users(skip=skip, limit=limit)

    def get_total_users_count(self) -> int:
        """Get total count of all users in the database.

        Returns:
            Total number of users.
        """
        return self.user_dao.count_all()

    def get_users_filtered(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        role_id: Optional[int] = None,
        is_active: Optional[bool] = None,
    ) -> tuple[List[User], int]:
        """Get users with filtering and pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search term for name or email (case-insensitive)
            role_id: Filter by role ID
            is_active: Filter by active status

        Returns:
            Tuple of (list of users, total count matching filters)
        """
        return self.user_dao.get_users_filtered(
            skip=skip,
            limit=limit,
            search=search,
            role_id=role_id,
            is_active=is_active,
        )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their unique identifier.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            User object if found, None otherwise.
        """
        return self.user_dao.get_by_id(user_id)

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information.

        Args:
            user_id: The unique identifier of the user to update.
            user_update: UserUpdate object containing the fields to update.
                Only non-None fields will be updated.

        Returns:
            Updated User object if found, None if user not found.
        """
        return self.user_dao.update_user(user_id, user_update)

    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate a user account.

        Sets the user's is_active status to False, preventing them from
        logging in or accessing protected resources.

        Args:
            user_id: The unique identifier of the user to deactivate.

        Returns:
            Updated User object if found, None if user not found.
        """
        user_update = UserUpdate(is_active=False)
        return self.user_dao.update_user(user_id, user_update)

    def activate_user(self, user_id: int) -> Optional[User]:
        """Activate a user account.

        Sets the user's is_active status to True, allowing them to
        log in and access protected resources.

        Args:
            user_id: The unique identifier of the user to activate.

        Returns:
            Updated User object if found, None if user not found.
        """
        user_update = UserUpdate(is_active=True)
        return self.user_dao.update_user(user_id, user_update)

    def create_user_without_verification(
        self, user_create: UserCreate, email_verified: bool = False
    ) -> User:
        """Create a user without sending verification email.

        Useful for seeding test/dummy users.

        Args:
            user_create: User creation data
            email_verified: Whether to mark the email as already verified

        Returns:
            The created user
        """
        # Check if user already exists
        if self.user_dao.get_by_email(user_create.email):
            raise UserAlreadyExistsError("Email already registered")

        # Create user (this sets email_verification_token in DAO)
        user = self.user_dao.create_user(user_create)

        # If email should be pre-verified, update it
        if email_verified:
            self.user_dao.set_email_verified(user.id, True)
            user = self.user_dao.get_by_id(user.id)

        return user

    def get_users_by_email_domain(self, domain: str) -> List[User]:
        """Get all users with emails matching a domain pattern.

        Args:
            domain: Email domain to match (e.g., "@dummyuser.com")

        Returns:
            List of users with matching email domain
        """
        return self.user_dao.get_users_by_email_domain(domain)

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID.

        Args:
            user_id: ID of the user to delete

        Returns:
            True if user was deleted, False if not found
        """
        return self.user_dao.delete_user(user_id)

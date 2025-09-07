from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, status

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
from app.service.user_service import UserService


class TestUserService:
    @pytest.fixture
    def mock_user_dao(self) -> Mock:
        """Create a mock UserDAO for testing."""
        return Mock(spec=UserDAO)

    @pytest.fixture
    def mock_email_service(self) -> Mock:
        """Create a mock EmailService for testing."""
        email_service = Mock(spec=EmailService)
        email_service.send_verification_email = AsyncMock()
        email_service.send_reset_password_email = AsyncMock()
        return email_service

    @pytest.fixture
    def mock_auth_service(self) -> Mock:
        """Create a mock AuthService for testing."""
        from app.service.auth_service import AuthService
        auth_service = Mock(spec=AuthService)
        auth_service.create_access_token.return_value = "fake_token"
        auth_service.ACCESS_TOKEN_EXPIRE_SECONDS = 30 * 60
        return auth_service

    @pytest.fixture
    def user_service(
        self, mock_user_dao: Mock, mock_email_service: Mock, mock_auth_service: Mock
    ) -> UserService:
        """Create a UserService instance with mocked DAO, EmailService, and AuthService."""
        return UserService(
            user_dao=mock_user_dao,
            email_service=mock_email_service,
            auth_service=mock_auth_service
        )

    @pytest.mark.asyncio
    async def test_register_user_success(
        self,
        user_service: UserService,
        mock_user_dao: Mock,
        mock_email_service: Mock,
        mock_auth_service: Mock,
        sample_user_create: UserCreate,
        sample_db_user: Mock,
    ) -> None:
        """Test successful user registration."""
        # Arrange
        mock_user_dao.get_by_email.return_value = None  # User doesn't exist
        mock_user_dao.create_user.return_value = sample_db_user

        # Act
        result = await user_service.register_user(sample_user_create)

        # Assert
        assert isinstance(result, UserWithAccessToken)
        assert result.user.email == sample_user_create.email
        mock_user_dao.get_by_email.assert_called_once_with(sample_user_create.email)
        mock_user_dao.create_user.assert_called_once_with(sample_user_create)
        # Verify email verification was sent
        mock_email_service.send_verification_email.assert_called_once_with(
            sample_db_user.email, sample_db_user.email_verification_token
        )
        # Verify access token was created
        mock_auth_service.create_access_token.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_user_already_exists(
        self,
        user_service: UserService,
        mock_user_dao: Mock,
        sample_user_create: UserCreate,
        sample_db_user: Mock,
    ) -> None:
        """Test registration fails when user already exists."""
        # Arrange
        mock_user_dao.get_by_email.return_value = sample_db_user  # User exists

        # Act & Assert
        with pytest.raises(UserAlreadyExistsError) as exc_info:
            await user_service.register_user(sample_user_create)

        assert str(exc_info.value) == "Email already registered"
        mock_user_dao.get_by_email.assert_called_once_with(sample_user_create.email)
        mock_user_dao.create_user.assert_not_called()

    def test_authenticate_user_success(
        self,
        user_service: UserService,
        mock_user_dao: Mock,
        mock_auth_service: Mock,
        sample_user_login: UserLogin,
        sample_db_user: Mock,
    ) -> None:
        """Test successful user authentication."""
        # Arrange
        mock_user_dao.authenticate.return_value = sample_db_user
        mock_user_dao.is_active.return_value = True

        # Act
        result = user_service.authenticate_user(sample_user_login)

        # Assert
        assert isinstance(result, Token)
        assert result.access_token == "fake_token"
        assert result.token_type == "bearer"
        assert result.expires_in == 30 * 60  # 30 minutes in seconds
        mock_user_dao.authenticate.assert_called_once_with(
            sample_user_login.email, sample_user_login.password
        )
        mock_user_dao.is_active.assert_called_once_with(sample_db_user)
        mock_auth_service.create_access_token.assert_called_once()

    def test_authenticate_user_invalid_credentials(
        self,
        user_service: UserService,
        mock_user_dao: Mock,
        sample_user_login: UserLogin,
    ) -> None:
        """Test authentication fails with invalid credentials."""
        # Arrange
        mock_user_dao.authenticate.return_value = None  # Authentication failed

        # Act & Assert
        with pytest.raises(InvalidCredentialsError) as exc_info:
            user_service.authenticate_user(sample_user_login)

        assert str(exc_info.value) == "Incorrect email or password"
        mock_user_dao.authenticate.assert_called_once_with(
            sample_user_login.email, sample_user_login.password
        )

    def test_authenticate_user_inactive(
        self,
        user_service: UserService,
        mock_user_dao: Mock,
        sample_user_login: UserLogin,
        sample_db_user: Mock,
    ) -> None:
        """Test authentication fails for inactive user."""
        # Arrange
        mock_user_dao.authenticate.return_value = sample_db_user
        mock_user_dao.is_active.return_value = False  # User is inactive

        # Act & Assert
        with pytest.raises(InactiveUserError) as exc_info:
            user_service.authenticate_user(sample_user_login)

        assert str(exc_info.value) == "User account is inactive"
        mock_user_dao.authenticate.assert_called_once_with(
            sample_user_login.email, sample_user_login.password
        )
        mock_user_dao.is_active.assert_called_once_with(sample_db_user)

    def test_get_user_by_email_success(
        self, user_service: UserService, mock_user_dao: Mock, sample_db_user: Mock
    ) -> None:
        """Test successfully getting user by email."""
        # Arrange
        email = "test@example.com"
        mock_user_dao.get_by_email.return_value = sample_db_user

        # Act
        result = user_service.get_user_by_email(email)

        # Assert
        assert isinstance(result, User)
        assert result.email == email
        mock_user_dao.get_by_email.assert_called_once_with(email)

    def test_get_user_by_email_not_found(
        self, user_service: UserService, mock_user_dao: Mock
    ) -> None:
        """Test getting user by email when user doesn't exist."""
        # Arrange
        email = "nonexistent@example.com"
        mock_user_dao.get_by_email.return_value = None

        # Act
        result = user_service.get_user_by_email(email)

        # Assert
        assert result is None
        mock_user_dao.get_by_email.assert_called_once_with(email)

    @pytest.mark.asyncio
    async def test_forgot_password_user_exists(
        self,
        user_service: UserService,
        mock_user_dao: Mock,
        mock_email_service: Mock,
        sample_db_user: Mock,
    ) -> None:
        """Test forgot password for existing user."""
        # Arrange
        forgot_password = ForgotPassword(email="test@example.com")
        reset_token = "reset_token_123"
        mock_user_dao.get_by_email.return_value = sample_db_user
        mock_user_dao.set_password_reset_token.return_value = reset_token

        # Act
        result = await user_service.forgot_password(forgot_password)

        # Assert
        assert result is None
        mock_user_dao.get_by_email.assert_called_once_with(forgot_password.email)
        mock_user_dao.set_password_reset_token.assert_called_once_with(
            forgot_password.email
        )
        # Verify password reset email was sent
        mock_email_service.send_reset_password_email.assert_called_once_with(
            forgot_password.email, reset_token
        )

    @pytest.mark.asyncio
    async def test_forgot_password_user_not_exists(
        self, user_service: UserService, mock_user_dao: Mock
    ) -> None:
        """Test forgot password for non-existing user."""
        # Arrange
        forgot_password = ForgotPassword(email="nonexistent@example.com")
        mock_user_dao.get_by_email.return_value = None

        # Act
        result = await user_service.forgot_password(forgot_password)

        # Assert
        assert result is None
        mock_user_dao.get_by_email.assert_called_once_with(forgot_password.email)
        mock_user_dao.set_password_reset_token.assert_not_called()

    def test_reset_password_success(
        self, user_service: UserService, mock_user_dao: Mock, sample_db_user: Mock
    ) -> None:
        """Test successful password reset."""
        # Arrange
        password_reset = PasswordReset(
            token="valid_token", new_password="new_password123"
        )
        mock_user_dao.reset_password_by_token.return_value = sample_db_user

        # Act
        result = user_service.reset_password(password_reset)

        # Assert
        assert result is None
        mock_user_dao.reset_password_by_token.assert_called_once_with(
            password_reset.token, password_reset.new_password
        )

    def test_reset_password_invalid_token(
        self, user_service: UserService, mock_user_dao: Mock
    ) -> None:
        """Test password reset with invalid token."""
        # Arrange
        password_reset = PasswordReset(
            token="invalid_token", new_password="new_password123"
        )
        mock_user_dao.reset_password_by_token.return_value = None

        # Act & Assert
        with pytest.raises(InvalidPasswordResetTokenError) as exc_info:
            user_service.reset_password(password_reset)

        assert str(exc_info.value) == "Invalid or expired reset token"
        mock_user_dao.reset_password_by_token.assert_called_once_with(
            password_reset.token, password_reset.new_password
        )

    def test_verify_email_success(
        self, user_service: UserService, mock_user_dao: Mock, mock_auth_service: Mock, sample_db_user: Mock
    ) -> None:
        """Test successful email verification."""
        # Arrange
        token = "valid_verification_token"
        mock_user_dao.verify_email.return_value = sample_db_user

        # Act
        result = user_service.verify_email(token)

        # Assert
        assert isinstance(result, UserWithAccessToken)
        mock_user_dao.verify_email.assert_called_once_with(token)
        mock_auth_service.create_access_token.assert_called_once()

    def test_verify_email_invalid_token(
        self, user_service: UserService, mock_user_dao: Mock
    ) -> None:
        """Test email verification with invalid token."""
        # Arrange
        token = "invalid_token"
        mock_user_dao.verify_email.return_value = None

        # Act & Assert
        with pytest.raises(InvalidVerificationTokenError) as exc_info:
            user_service.verify_email(token)

        assert str(exc_info.value) == "Invalid or expired verification token"
        mock_user_dao.verify_email.assert_called_once_with(token)

    def test_user_service_with_custom_dao(
        self, mock_user_dao: Mock, mock_email_service: Mock
    ) -> None:
        """Test that UserService can be created with custom DAO and EmailService."""
        # Act
        service = UserService(user_dao=mock_user_dao, email_service=mock_email_service)

        # Assert
        assert service.user_dao is mock_user_dao
        assert service.email_service is mock_email_service

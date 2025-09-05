from unittest.mock import Mock, patch

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
)
from app.service.user_service import UserService


class TestUserService:
    @pytest.fixture
    def mock_user_dao(self) -> Mock:
        """Create a mock UserDAO for testing."""
        return Mock(spec=UserDAO)

    @pytest.fixture
    def user_service(self, mock_user_dao: Mock) -> UserService:
        """Create a UserService instance with mocked DAO."""
        return UserService(user_dao=mock_user_dao)

    def test_register_user_success(
        self,
        user_service: UserService,
        mock_user_dao: Mock,
        sample_user_create: UserCreate,
        sample_db_user: Mock,
    ) -> None:
        """Test successful user registration."""
        # Arrange
        mock_user_dao.get_by_email.return_value = None  # User doesn't exist
        mock_user_dao.create_user.return_value = sample_db_user

        # Act
        result = user_service.register_user(sample_user_create)

        # Assert
        assert isinstance(result, User)
        assert result.email == sample_user_create.email
        mock_user_dao.get_by_email.assert_called_once_with(sample_user_create.email)
        mock_user_dao.create_user.assert_called_once_with(sample_user_create)

    def test_register_user_already_exists(
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
        with pytest.raises(HTTPException) as exc_info:
            user_service.register_user(sample_user_create)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in str(exc_info.value.detail)
        mock_user_dao.get_by_email.assert_called_once_with(sample_user_create.email)
        mock_user_dao.create_user.assert_not_called()

    @patch("app.service.user_service.create_access_token")
    def test_authenticate_user_success(
        self,
        mock_create_token: Mock,
        user_service: UserService,
        mock_user_dao: Mock,
        sample_user_login: UserLogin,
        sample_db_user: Mock,
    ) -> None:
        """Test successful user authentication."""
        # Arrange
        mock_user_dao.authenticate.return_value = sample_db_user
        mock_user_dao.is_active.return_value = True
        mock_create_token.return_value = "fake_token"

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
        with pytest.raises(HTTPException) as exc_info:
            user_service.authenticate_user(sample_user_login)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in str(exc_info.value.detail)
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
        with pytest.raises(HTTPException) as exc_info:
            user_service.authenticate_user(sample_user_login)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Inactive user" in str(exc_info.value.detail)
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

    def test_forgot_password_user_exists(
        self, user_service: UserService, mock_user_dao: Mock, sample_db_user: Mock
    ) -> None:
        """Test forgot password for existing user."""
        # Arrange
        forgot_password = ForgotPassword(email="test@example.com")
        mock_user_dao.get_by_email.return_value = sample_db_user

        # Act
        result = user_service.forgot_password(forgot_password)

        # Assert
        assert (
            result["message"]
            == "If the email exists, a password reset link has been sent"
        )
        mock_user_dao.get_by_email.assert_called_once_with(forgot_password.email)
        mock_user_dao.set_password_reset_token.assert_called_once_with(
            forgot_password.email
        )

    def test_forgot_password_user_not_exists(
        self, user_service: UserService, mock_user_dao: Mock
    ) -> None:
        """Test forgot password for non-existing user."""
        # Arrange
        forgot_password = ForgotPassword(email="nonexistent@example.com")
        mock_user_dao.get_by_email.return_value = None

        # Act
        result = user_service.forgot_password(forgot_password)

        # Assert
        assert (
            result["message"]
            == "If the email exists, a password reset link has been sent"
        )
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
        assert result["message"] == "Password reset successfully"
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
        with pytest.raises(HTTPException) as exc_info:
            user_service.reset_password(password_reset)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid or expired reset token" in str(exc_info.value.detail)
        mock_user_dao.reset_password_by_token.assert_called_once_with(
            password_reset.token, password_reset.new_password
        )

    def test_verify_email_success(
        self, user_service: UserService, mock_user_dao: Mock, sample_db_user: Mock
    ) -> None:
        """Test successful email verification."""
        # Arrange
        token = "valid_verification_token"
        mock_user_dao.verify_email.return_value = sample_db_user

        # Act
        result = user_service.verify_email(token)

        # Assert
        assert result["message"] == "Email verified successfully"
        mock_user_dao.verify_email.assert_called_once_with(token)

    def test_verify_email_invalid_token(
        self, user_service: UserService, mock_user_dao: Mock
    ) -> None:
        """Test email verification with invalid token."""
        # Arrange
        token = "invalid_token"
        mock_user_dao.verify_email.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            user_service.verify_email(token)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid verification token" in str(exc_info.value.detail)
        mock_user_dao.verify_email.assert_called_once_with(token)

    def test_user_service_with_custom_dao(self, mock_user_dao: Mock) -> None:
        """Test that UserService can be created with custom DAO."""
        # Act
        service = UserService(user_dao=mock_user_dao)

        # Assert
        assert service.user_dao is mock_user_dao

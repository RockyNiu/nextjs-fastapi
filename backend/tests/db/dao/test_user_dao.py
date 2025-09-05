from datetime import datetime, timedelta, timezone
from typing import Optional
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from app.core.security import (
    get_password_hash,
)
from app.db.dao.user_dao import UserDAO
from app.db.orm.user_orm import UserORM
from app.entities.user import User, UserCreate
from tests.db.dao.dao_test import DaoTest


class TestUserDAO(DaoTest):
    """Test class for UserDAO functionality following the established pattern."""

    def init_dao(self) -> None:
        """Initialize the DAO for testing."""
        self.dao: Optional[UserDAO] = None  # Will be set in individual tests

    def test_init_with_provided_session(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test UserDAO initialization with a provided session."""
        dao = UserDAO(test_session)

        assert dao.session is test_session
        assert isinstance(dao, UserDAO)

    def test_init_without_session(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test UserDAO initialization without session uses default."""
        with patch(
            "app.db.database.DatabaseManager.get_session", return_value=test_session
        ):
            dao = UserDAO()

            assert dao.session is test_session

    def test_get_by_email_existing_user(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test getting an existing user by email."""
        # Create a mock user ORM in the database
        mock_user_orm = UserORM(
            id=1,
            email="test@example.com",
            hashed_password="hashed_password",
            first_name="John",
            last_name="Doe",
            is_active=True,
            email_verified=False,
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )

        # Mock the query chain
        with patch.object(test_session, "query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = (
                mock_user_orm
            )

            dao = UserDAO(test_session)
            result = dao.get_by_email("test@example.com")

            # Should return User, not UserORM
            assert isinstance(result, User)
            assert result.email == "test@example.com"
            assert result.first_name == "John"
            assert result.last_name == "Doe"
            mock_query.assert_called_once_with(UserORM)
            mock_query.return_value.filter.assert_called_once()
            mock_query.return_value.filter.return_value.first.assert_called_once()

    def test_get_by_email_non_existent_user(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test getting a non-existent user by email returns None."""
        with patch.object(test_session, "query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = None

            dao = UserDAO(test_session)
            result = dao.get_by_email("nonexistent@example.com")

            assert result is None

    def test_create_user_success(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test successful user creation."""
        user_create = UserCreate(
            email="newuser@example.com",
            password="securepassword123",
            first_name="Jane",
            last_name="Smith",
            is_active=True,
        )

        with patch.object(test_session, "add") as mock_add:
            with patch.object(test_session, "flush") as mock_flush:
                # Mock flush to set the ID on the user object
                def mock_flush_func():
                    # Simulate database setting an ID after flush
                    mock_add.call_args[0][0].id = 1
                    mock_add.call_args[0][0].date_created = datetime.now(timezone.utc)
                    mock_add.call_args[0][0].date_updated = datetime.now(timezone.utc)
                    mock_add.call_args[0][0].email_verified = False

                mock_flush.side_effect = mock_flush_func

                dao = UserDAO(test_session)
                result = dao.create_user(user_create)

                # Should return User entity
                assert isinstance(result, User)
                assert result.email == "newuser@example.com"
                assert result.first_name == "Jane"
                assert result.last_name == "Smith"
                assert result.is_active is True
                # User should have these attributes
                assert hasattr(result, "email_verified")
                assert hasattr(result, "email_verification_token")

                # Verify session methods were called
                mock_add.assert_called_once()
                mock_flush.assert_called_once()

    def test_authenticate_success(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test successful user authentication."""
        # Create UserORM for testing - since authenticate queries UserORM directly

        hashed_password = get_password_hash("correct_password")
        mock_user_orm = UserORM(
            id=1,
            email="user@example.com",
            hashed_password=hashed_password,
            first_name="John",
            last_name="Doe",
            is_active=True,
            email_verified=False,
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )

        dao = UserDAO(test_session)

        # Mock the session.execute method
        with patch.object(test_session, "execute") as mock_execute:
            mock_result = Mock()
            mock_result.scalar_one_or_none.return_value = mock_user_orm
            mock_execute.return_value = mock_result

            result = dao.authenticate("user@example.com", "correct_password")

            # Should return User entity
            assert isinstance(result, User)
            assert result.email == "user@example.com"

    def test_authenticate_user_not_found(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test authentication with non-existent user."""
        dao = UserDAO(test_session)

        # Mock the session.execute method to return None (user not found)
        with patch.object(test_session, "execute") as mock_execute:
            mock_result = Mock()
            mock_result.scalar_one_or_none.return_value = None
            mock_execute.return_value = mock_result

            result = dao.authenticate("nonexistent@example.com", "password")

            assert result is None

    def test_authenticate_wrong_password(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test authentication with wrong password."""
        # Create UserORM for testing - since authenticate queries UserORM directly

        hashed_password = get_password_hash("correct_password")
        mock_user_orm = UserORM(
            id=1,
            email="user@example.com",
            hashed_password=hashed_password,
            first_name="John",
            last_name="Doe",
            is_active=True,
            email_verified=False,
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )

        dao = UserDAO(test_session)

        # Mock the session.execute method
        with patch.object(test_session, "execute") as mock_execute:
            mock_result = Mock()
            mock_result.scalar_one_or_none.return_value = mock_user_orm
            mock_execute.return_value = mock_result

            result = dao.authenticate("user@example.com", "wrong_password")

            assert result is None

    def test_is_active_true(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test is_active returns True for active user."""
        mock_user = User(
            id=1,
            email="user@example.com",
            first_name="John",
            last_name="Doe",
            is_active=True,
            email_verified=False,
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        dao = UserDAO(test_session)

        result = dao.is_active(mock_user)

        assert result is True

    def test_is_active_false(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test is_active returns False for inactive user."""
        mock_user = User(
            id=1,
            email="user@example.com",
            first_name="John",
            last_name="Doe",
            is_active=False,
            email_verified=False,
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )
        dao = UserDAO(test_session)

        result = dao.is_active(mock_user)

        assert result is False

    def test_set_password_reset_token(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test setting password reset token."""
        mock_user_orm = UserORM(email="user@example.com")
        dao = UserDAO(test_session)

        with patch.object(test_session, "query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = (
                mock_user_orm
            )

            result = dao.set_password_reset_token("user@example.com")

            # Verify a token was generated (it should be a string)
            assert isinstance(result, str)
            assert len(result) > 0
            assert mock_user_orm.password_reset_token == result  # type: ignore
            assert mock_user_orm.password_reset_expires is not None  # type: ignore

    def test_reset_password_by_token_success(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test successful password reset by token."""
        mock_user_orm = UserORM(
            id=1,
            email="user@example.com",
            first_name="John",
            last_name="Doe",
            is_active=True,
            email_verified=False,
            password_reset_token="valid_token",
            password_reset_expires=datetime.now(timezone.utc) + timedelta(hours=1),
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )

        with patch.object(test_session, "query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = (
                mock_user_orm
            )
            dao = UserDAO(test_session)

            result = dao.reset_password_by_token("valid_token", "new_password")

            # Should return User entity
            assert isinstance(result, User)
            # Verify password was changed (should be a hashed password)
            assert isinstance(mock_user_orm.hashed_password, str)  # type: ignore
            assert len(mock_user_orm.hashed_password) > 10  # type: ignore  # Hashed passwords are long
            assert mock_user_orm.password_reset_token is None  # type: ignore
            assert mock_user_orm.password_reset_expires is None  # type: ignore

    def test_reset_password_by_token_invalid_token(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test password reset with invalid token."""
        with patch.object(test_session, "query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = None

            dao = UserDAO(test_session)
            result = dao.reset_password_by_token("invalid_token", "new_password")

            assert result is None

    def test_reset_password_by_token_expired(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test password reset with expired token."""
        # Token that expired 1 hour ago
        expired_time = datetime.now(timezone.utc) - timedelta(hours=1)
        UserORM(
            email="user@example.com",
            password_reset_token="expired_token",
            password_reset_expires=expired_time,
        )

        with patch.object(test_session, "query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = (
                None  # Query would return None for expired token
            )

            dao = UserDAO(test_session)
            result = dao.reset_password_by_token("expired_token", "new_password")

            assert result is None

    def test_verify_email_success(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test successful email verification."""
        mock_user_orm = UserORM(
            id=1,
            email="user@example.com",
            first_name="John",
            last_name="Doe",
            is_active=True,
            email_verified=False,
            email_verification_token="verification_token",
            date_created=datetime.now(timezone.utc),
            date_updated=datetime.now(timezone.utc),
        )

        with patch.object(test_session, "query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = (
                mock_user_orm
            )

            dao = UserDAO(test_session)
            result = dao.verify_email("verification_token")

            # Should return User entity
            assert isinstance(result, User)
            assert mock_user_orm.email_verified is True  # type: ignore
            assert mock_user_orm.email_verification_token is None  # type: ignore

    def test_verify_email_invalid_token(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test email verification with invalid token."""
        with patch.object(test_session, "query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = None

            dao = UserDAO(test_session)
            result = dao.verify_email("invalid_token")

            assert result is None

    def test_inheritance_from_base_dao(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test that UserDAO properly inherits from BaseDAO."""
        dao = UserDAO(test_session)

        # Test that it has the session attribute from BaseDAO
        assert hasattr(dao, "session")
        assert dao.session is test_session

        # Test that it's an instance of both UserDAO and its parent
        assert isinstance(dao, UserDAO)
        from app.db.dao.base_dao import BaseDAO

        assert isinstance(dao, BaseDAO)

from typing import Optional
from unittest.mock import Mock, patch

import pytest
from sqlalchemy.orm import Session

from app.db.dao.base_dao import BaseDAO
from app.db.database import DatabaseManager, DatabaseSessionNotInitializedError
from app.db.orm.user_orm import UserORM
from app.entities.user import UserCreate
from tests.db.dao.dao_test import DaoTest


class TestBaseDAO(DaoTest):
    """Test class for BaseDAO functionality following the established pattern."""

    def init_dao(self) -> None:
        """Initialize the DAO for testing."""
        self.dao: Optional[BaseDAO] = (
            None  # BaseDAO is abstract, we'll create instances in individual tests
        )

    def test_init_with_provided_session(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test BaseDAO initialization with a provided session."""
        dao = BaseDAO(session=test_session)

        assert dao.session is test_session
        assert dao.session == test_session

    def test_init_without_session_uses_database_manager(
        self, test_session: Session
    ) -> None:  # type: ignore[misc]
        """Test BaseDAO initialization without session uses DatabaseManager."""
        with patch.object(
            DatabaseManager, "get_session", return_value=test_session
        ) as mock_get_session:
            dao = BaseDAO()

            assert dao.session is test_session
            mock_get_session.assert_called_once()

    def test_init_with_none_session_uses_database_manager(
        self, test_session: Session
    ) -> None:  # type: ignore[misc]
        """Test BaseDAO initialization with None session uses DatabaseManager."""
        with patch.object(
            DatabaseManager, "get_session", return_value=test_session
        ) as mock_get_session:
            dao = BaseDAO(session=None)

            assert dao.session is test_session
            mock_get_session.assert_called_once()

    def test_database_session_not_initialized_error_handling(self) -> None:  # type: ignore[misc]
        """Test BaseDAO handles DatabaseSessionNotInitializedError properly."""
        with patch.object(
            DatabaseManager,
            "get_session",
            side_effect=DatabaseSessionNotInitializedError(),
        ):
            with pytest.raises(DatabaseSessionNotInitializedError):
                BaseDAO()

    def test_session_attribute_access(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test that session attribute is properly accessible."""
        dao = BaseDAO(session=test_session)

        # Test that we can access session attributes
        assert hasattr(dao, "session")
        assert isinstance(dao.session, Session)

        # Test session is the same object
        assert dao.session is test_session

    def test_multiple_dao_instances_with_different_sessions(self) -> None:  # type: ignore[misc]
        """Test creating multiple BaseDAO instances with different sessions."""
        session1 = Mock(spec=Session)
        session2 = Mock(spec=Session)

        dao1 = BaseDAO(session=session1)
        dao2 = BaseDAO(session=session2)

        assert dao1.session is session1
        assert dao2.session is session2
        assert dao1.session is not dao2.session

    def test_session_type_validation(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test that session is properly typed."""
        dao = BaseDAO(session=test_session)

        assert isinstance(dao.session, Session)

    def test_database_manager_integration(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test integration with DatabaseManager."""
        with patch.object(DatabaseManager, "_initialized", True):
            with patch.object(
                DatabaseManager, "get_session", return_value=test_session
            ) as mock_get_session:
                dao = BaseDAO()

                # Verify DatabaseManager.get_session was called
                mock_get_session.assert_called_once()

                # Verify session is set correctly
                assert dao.session is test_session

    def test_pydantic_model_validation_integration(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test BaseDAO works correctly with Pydantic models."""
        BaseDAO(session=test_session)

        # Test creating a valid Pydantic model
        user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe",
            "is_active": True,
        }

        # Validate Pydantic model creation works
        user_create = UserCreate(**user_data)
        assert user_create.email == "test@example.com"
        assert user_create.first_name == "John"
        assert user_create.last_name == "Doe"
        assert user_create.is_active is True

        # Test model serialization
        user_dict = user_create.model_dump()
        assert isinstance(user_dict, dict)
        assert "email" in user_dict
        assert "password" in user_dict


class ConcreteDAO(BaseDAO):
    """Concrete implementation of BaseDAO for testing inheritance."""

    def some_method(self) -> str:
        """Dummy method to test inheritance."""
        return "concrete_dao_method"


class TestBaseDaoInheritance(DaoTest):
    """Test BaseDAO inheritance patterns."""

    def init_dao(self) -> None:
        """Initialize the concrete DAO for testing."""
        self.dao: Optional[ConcreteDAO] = None  # Will be set in individual tests

    def test_concrete_dao_inherits_session_management(
        self, test_session: Session
    ) -> None:  # type: ignore[misc]
        """Test that concrete DAOs inherit session management."""
        dao = ConcreteDAO(session=test_session)

        assert dao.session is test_session
        assert hasattr(dao, "some_method")
        assert dao.some_method() == "concrete_dao_method"

    def test_concrete_dao_without_session(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test concrete DAO without provided session."""
        with patch.object(DatabaseManager, "get_session", return_value=test_session):
            dao = ConcreteDAO()

            assert dao.session is test_session
            assert dao.some_method() == "concrete_dao_method"

    def test_concrete_dao_method_can_use_session(self, test_session: Session) -> None:  # type: ignore[misc]
        """Test that concrete DAO methods can access the session."""
        dao = ConcreteDAO(session=test_session)

        # Verify session is accessible from within the DAO
        assert dao.session is test_session

        # Test that session methods can be called (mock to avoid actual DB operations)
        with patch.object(test_session, "query") as mock_query:
            mock_query.return_value = "mocked_query_result"

            # This would typically be in a real DAO method
            result = dao.session.query(UserORM)

            assert result == "mocked_query_result"
            mock_query.assert_called_once_with(UserORM)

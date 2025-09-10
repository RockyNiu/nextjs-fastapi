"""Integration tests that require a real database connection."""

import pytest
from app.db.database import DatabaseManager
from app.db.dao.user_dao import UserDAO
from app.entities.user import UserCreate


class TestDatabaseIntegration:
    """Test database operations with real database."""

    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Ensure database is properly initialized for each test."""
        DatabaseManager.initialize()
        yield
        # Cleanup after test if needed

    def test_database_connection(self):
        """Test that we can connect to the database."""
        # This will fail if database is not accessible
        user_dao = UserDAO()
        assert user_dao.session is not None

    def test_user_creation_and_retrieval(self):
        """Test creating and retrieving a user from the database."""
        user_dao = UserDAO()
        
        # Create test user
        user_create = UserCreate(
            email="integration-test@example.com",
            first_name="Integration",
            last_name="Test",
            password="testpassword123"
        )
        
        # Clean up existing test user if any
        existing_user = user_dao.get_by_email(user_create.email)
        if existing_user:
            user_dao.session.delete(existing_user)
            user_dao.session.commit()
        
        # Create new user
        created_user = user_dao.create_user(user_create)
        assert created_user is not None
        assert created_user.email == user_create.email
        
        # Retrieve user
        retrieved_user = user_dao.get_by_email(user_create.email)
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        
        # Clean up
        user_dao.session.delete(created_user)
        user_dao.session.commit()

    def test_user_authentication_flow(self):
        """Test complete user authentication flow."""
        user_dao = UserDAO()
        
        user_create = UserCreate(
            email="auth-test@example.com",
            first_name="Auth",
            last_name="Test",
            password="testpassword123"
        )
        
        # Clean up existing test user if any
        existing_user = user_dao.get_by_email(user_create.email)
        if existing_user:
            user_dao.session.delete(existing_user)
            user_dao.session.commit()
        
        # Create user
        created_user = user_dao.create_user(user_create)
        
        # Test authentication
        authenticated_user = user_dao.authenticate(user_create.email, user_create.password)
        assert authenticated_user is not None
        assert authenticated_user.id == created_user.id
        
        # Test wrong password
        wrong_auth = user_dao.authenticate(user_create.email, "wrongpassword")
        assert wrong_auth is None
        
        # Clean up
        user_dao.session.delete(created_user)
        user_dao.session.commit()
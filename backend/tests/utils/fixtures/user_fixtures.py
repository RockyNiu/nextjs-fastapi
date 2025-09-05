from datetime import datetime
from unittest.mock import Mock

import pytest

from app.entities.user import UserCreate, UserLogin


@pytest.fixture
def sample_user_create() -> UserCreate:
    """Sample user creation data."""
    return UserCreate(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        password="password123",
    )


@pytest.fixture
def sample_user_login() -> UserLogin:
    """Sample user login data."""
    return UserLogin(email="test@example.com", password="password123")


@pytest.fixture
def sample_db_user() -> Mock:
    """Sample database user object."""
    mock_user = Mock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.first_name = "John"
    mock_user.last_name = "Doe"
    mock_user.is_active = True
    mock_user.date_created = datetime(2023, 1, 1, 0, 0, 0)
    mock_user.date_updated = datetime(2023, 1, 1, 0, 0, 0)
    mock_user.email_verified = False
    mock_user.email_verification_token = "some_token"
    mock_user.password_reset_token = None
    mock_user.password_reset_expires = None
    return mock_user


@pytest.fixture
def sample_user_create_admin() -> UserCreate:
    """Sample admin user creation data."""
    return UserCreate(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        password="admin123456",
    )


@pytest.fixture
def sample_inactive_user() -> Mock:
    """Sample inactive database user object."""
    mock_user = Mock()
    mock_user.id = 2
    mock_user.email = "inactive@example.com"
    mock_user.first_name = "Inactive"
    mock_user.last_name = "User"
    mock_user.is_active = False
    mock_user.date_created = datetime(2023, 1, 1, 0, 0, 0)
    mock_user.date_updated = datetime(2023, 1, 1, 0, 0, 0)
    mock_user.email_verified = True
    mock_user.email_verification_token = None
    mock_user.password_reset_token = None
    mock_user.password_reset_expires = None
    return mock_user

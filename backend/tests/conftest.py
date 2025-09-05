import os
import sys
from pathlib import Path
from typing import Generator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Set test environment
os.environ["BACKEND_ENV"] = "test"

# Import after setting up the path
from app.config import ConfigLoader
from app.db.database import current_database_session
from app.db.orm.base_orm import BaseORM


@pytest.fixture(scope="session")
def test_engine() -> Generator[Engine, None, None]:
    """Create a test database engine using the main database."""
    config = ConfigLoader.get_config()
    # Use the main database URL for tests
    test_db_url = config.endpoint_url

    engine = create_engine(test_db_url, echo=False)  # Disable echo in tests

    # Ensure all tables exist (but don't drop/recreate)
    BaseORM.metadata.create_all(engine)

    yield engine

    # Clean up engine resources
    engine.dispose()


@pytest.fixture
def test_session(test_engine: Engine) -> Generator[Session, None, None]:
    """Create a test database session with proper cleanup."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    # Set the test session as the current session
    current_database_session.set(session)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def db_session(test_session: Session) -> Session:
    """Alias for test_session for easier use in tests."""
    return test_session

from abc import ABC, abstractmethod

import pytest
from sqlalchemy.orm import Session


class DaoTest(ABC):
    @abstractmethod
    def init_dao(self):
        """Initialize the DAO for testing."""
        pass

    @pytest.fixture(autouse=True)
    def _setup_test_session(self, test_session: Session):
        """Set up the test session for each test method."""
        self.init_dao()
        yield
        # Session cleanup is handled by the test_session fixture

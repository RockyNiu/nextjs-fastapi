from abc import ABC, abstractmethod

import pytest
from sqlalchemy.orm import Session

from app.db.database import DatabaseManager, current_database_session


class DaoTest(ABC):
    @classmethod
    def setup_class(cls):
        # Initialize the database session
        DatabaseManager._initialized = False
        DatabaseManager.initialize()

    def setup_method(self):
        pass

    @abstractmethod
    def init_dao(self):
        pass

    @pytest.fixture(autouse=True)
    def _start_database_session(self):
        with Session(DatabaseManager.engine) as session:
            try:
                current_database_session.set(session)
                self.init_dao()
                yield
            finally:
                session.rollback()

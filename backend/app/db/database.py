import logging
from contextlib import contextmanager
from contextvars import ContextVar

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.config import ConfigLoader

current_database_session: ContextVar[Session] = ContextVar("current_database_session")


class DatabaseSessionNotInitializedError(Exception):
    """
    Exception raised when trying to access the database session without initializing it first.
    """

    def __init__(self):
        super().__init__(
            "Database session not initialized. Use `DatabaseManager.get_session()` to initialize it."
        )


class DatabaseManager:
    _initialized = False

    engine: Engine
    endpoint_url: str

    @classmethod
    def initialize(cls):
        if not cls._initialized:
            config = ConfigLoader.get_config().mysql
            cls.endpoint_url = f"mysql+mysqlconnector://{config.username}:{config.password}@{config.host}:{config.port}/{config.dbname}?charset=utf8mb4"
            # Create the database engine. The connnection only happens the first time a task is performaed against the database.
            cls.engine = create_engine(cls.endpoint_url, echo=True)
            cls._initialized = True

    @classmethod
    def get_session(cls) -> Session:
        """
        Get the current database session. If the session is not initialized, raise an error.

        Returns:
          Session: The current database session.

        """
        session = current_database_session.get(None)
        if session is None:
            raise DatabaseSessionNotInitializedError()
        return session


@contextmanager
def database_context():
    """
    Context manager that provides a database session to the block inside it.
    """
    with Session(DatabaseManager.engine) as session:
        try:
            current_database_session.set(session)
            logging.debug(f"Starting database session: [{session}]")
            yield
            logging.debug(f"Committing database session: [{session}]")
            session.commit()
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            session.rollback()
            raise e


DatabaseManager.initialize()

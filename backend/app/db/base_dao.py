from typing import Optional

from backend.app.db.database import DatabaseManager
from sqlalchemy.orm import Session


class BaseDAO:
    session: Session

    def __init__(self, session: Optional[Session] = None):
        self.session = session or DatabaseManager.get_session()

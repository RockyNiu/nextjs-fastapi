from typing import Optional

from sqlalchemy.orm import Session

from backend.app.database import DatabaseManager



class BaseDAO:
  session: Session

  def __init__(self, session: Optional[Session] = None):
    self.session = session or DatabaseManager.get_session()

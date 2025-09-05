import sqlalchemy_utc
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.orm.base_orm import BaseORM


class UserORM(BaseORM):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    email_verification_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    date_created = Column(
        sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )
    date_updated = Column(
        sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

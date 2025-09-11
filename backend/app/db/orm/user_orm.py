from datetime import datetime
from enum import StrEnum
from typing import Optional

import sqlalchemy_utc
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.orm.base_orm import BaseORM


class UserRole(StrEnum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class UserORM(BaseORM):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER, nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_verification_token: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    password_reset_token: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    password_reset_expires: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    date_created: Mapped[datetime] = mapped_column(
        sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )
    date_updated: Mapped[datetime] = mapped_column(
        sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

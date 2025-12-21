from datetime import datetime
from typing import Optional

import sqlalchemy_utc
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.orm.base_orm import BaseORM
from app.db.orm.user_role_orm import RefUserRole, UserRole


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
    role_id: Mapped[UserRole] = mapped_column(
        ForeignKey("ref_user_role.id"), default=UserRole.USER, nullable=False
    )
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

    # Relationship to role
    role: Mapped[RefUserRole] = relationship("RefUserRole")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

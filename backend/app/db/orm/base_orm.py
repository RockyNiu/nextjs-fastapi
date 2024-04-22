from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy_utc import UtcDateTime, utcnow


class BaseORM(DeclarativeBase):
    pass


class DateCreatedUpdatedORM(DeclarativeBase):
    date_created = mapped_column(
        UtcDateTime,
        default=utcnow(),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    date_updated = mapped_column(
        UtcDateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        onupdate=utcnow(),
        nullable=False,
    )

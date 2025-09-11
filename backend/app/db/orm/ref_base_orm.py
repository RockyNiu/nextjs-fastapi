from typing import Generic, TypeVar

from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column

from app.db.orm.base_orm import BaseORM

T = TypeVar("T")


@declarative_mixin
class RefBaseORM(BaseORM, Generic[T]):
    """Base class for reference tables.

    Uses generics to define the enumeration type for the ID column. Value column must
    be unique.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String(50), nullable=False)
    __table_args__ = (UniqueConstraint("value", name="value"),)

from sqlalchemy import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from app.db.orm.base_orm import BaseORM, DateCreatedUpdatedORM


class ItemORM(BaseORM, DateCreatedUpdatedORM):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )

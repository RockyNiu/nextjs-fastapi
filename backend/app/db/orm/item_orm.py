from sqlalchemy import VARCHAR
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from app.db.orm.base_orm import BaseORM, DateCreatedUpdatedORM


class ItemORM(BaseORM, DateCreatedUpdatedORM):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )

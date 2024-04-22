from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base_dao import BaseDAO
from app.db.orm.item_orm import ItemORM
from app.entities.item import Item


class ItemDAO(BaseDAO):
    def __init__(self, session: Optional[Session] = None):
        super().__init__(session)

    def get_items(self) -> list[Item]:
        stmt = select(ItemORM).order_by(ItemORM.date_updated.desc())

        item_orms = self.session.execute(stmt).scalars().all()
        return [Item.model_validate(item_orm) for item_orm in item_orms]

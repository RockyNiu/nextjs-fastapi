from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base_dao import BaseDAO
from app.db.orm.item_orm import ItemORM
from app.entities.item import Item, ItemCreate, ItemUpdate


class ItemDAO(BaseDAO):
    def __init__(self, session: Optional[Session] = None):
        super().__init__(session)

    def get_items(self) -> list[Item]:
        stmt = select(ItemORM).order_by(ItemORM.date_updated.desc())

        item_orms = self.session.execute(stmt).scalars().all()
        return [Item.model_validate(item_orm) for item_orm in item_orms]

    def create_item(self, item: ItemCreate) -> Item:
        item_orm = ItemORM(
            name=item.name,
        )
        self.session.add(item_orm)
        self.session.flush()
        self.session.refresh(item_orm)
        return Item.model_validate(item_orm)

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        stmt = select(ItemORM).where(ItemORM.id == item_id)
        item_orm = self.session.execute(stmt).scalar_one_or_none()
        if item_orm is None:
            return None
        return Item.model_validate(item_orm)

    def update_item(self, item: ItemUpdate) -> Item:
        item_id = item.id
        stmt = select(ItemORM).where(ItemORM.id == item_id)
        item_orm = self.session.execute(stmt).scalar_one_or_none()
        if item_orm is None:
            raise ValueError(f"Item with id {item_id} not found")
        item_orm.name = item.name
        self.session.flush()
        self.session.refresh(item_orm)
        return Item.model_validate(item_orm)

    def delete_item(self, item_id: int) -> None:
        stmt = select(ItemORM).where(ItemORM.id == item_id)
        item_orm = self.session.execute(stmt).scalar_one_or_none()
        if item_orm is None:
            raise ValueError(f"Item with id {item_id} not found")
        self.session.delete(item_orm)
        self.session.flush()

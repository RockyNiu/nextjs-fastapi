from typing import List, Optional

from app.db.dao.item_dao import ItemDAO
from app.entities.item import Item, ItemCreate, ItemUpdate


class ItemService:
    item_dao: ItemDAO

    def __init__(self, item_dao: Optional[ItemDAO] = None) -> None:
        self.item_dao = item_dao or ItemDAO()

    def get_items(self) -> List[Item]:
        return self.item_dao.get_items()

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        return self.item_dao.get_item_by_id(item_id)

    def create_item(self, item: ItemCreate) -> Item:
        return self.item_dao.create_item(item)

    def update_item(self, item: ItemUpdate) -> Item:
        return self.item_dao.update_item(item)

    def delete_item(self, item_id: int) -> None:
        return self.item_dao.delete_item(item_id)

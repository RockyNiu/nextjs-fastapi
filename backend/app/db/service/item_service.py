from typing import List, Optional

from app.db.dao.item_dao import ItemDAO
from app.entities.item import Item


class ItemService:
    item_dao: ItemDAO

    def __init__(self, item_dao: Optional[ItemDAO] = None) -> None:
        self.item_dao = item_dao or ItemDAO()

    def get_items(self) -> List[Item]:
        return self.item_dao.get_items()

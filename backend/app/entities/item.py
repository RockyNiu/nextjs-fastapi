from app.entities.base import BaseEntity, DateCreatedUpdateEntity


class ItemCreate(BaseEntity):
    name: str


class ItemUpdate(BaseEntity):
    id: int
    name: str


class Item(ItemCreate, DateCreatedUpdateEntity):
    id: int

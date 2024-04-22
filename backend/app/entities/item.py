from app.entities.base import DateCreatedUpdateEntity


class Item(DateCreatedUpdateEntity):
    id: int
    name: str

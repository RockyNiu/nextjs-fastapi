import pytest
from backend.app.db.dao.item_dao import ItemDAO
from backend.app.entities.item import Item, ItemCreate
from faker import Faker


@pytest.fixture
def any_item_create() -> ItemCreate:
    faker = Faker()
    return ItemCreate(
        name=faker.name(),
    )


@pytest.fixture
def any_item() -> Item:
    faker = Faker()
    return Item(
        id=faker.random_int(),
        name=faker.name(),
        date_created=faker.date_time(),
        date_updated=faker.date_time(),
    )


@pytest.fixture
def persisted_item(any_item_create: ItemCreate) -> Item:
    item_dao = ItemDAO()
    return item_dao.create_item(any_item_create)

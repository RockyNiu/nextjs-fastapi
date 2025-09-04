import pytest
from sqlalchemy.orm import Session
from app.db.dao.item_dao import ItemDAO
from app.entities.item import Item, ItemCreate
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
        id=faker.random_int(
            min=1000000, max=9999999
        ),  # Use high numbers to avoid conflicts
        name=faker.name(),
        date_created=faker.date_time(),
        date_updated=faker.date_time(),
    )


@pytest.fixture
def persisted_item(any_item_create: ItemCreate, test_session: Session) -> Item:
    """Create a persisted item in the test database."""
    item_dao = ItemDAO()
    return item_dao.create_item(any_item_create)

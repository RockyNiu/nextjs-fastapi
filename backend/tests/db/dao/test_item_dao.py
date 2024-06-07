from app.db.dao.item_dao import ItemDAO
from app.entities.item import Item, ItemCreate, ItemUpdate
from tests.db.dao_test import DaoTest


class TestItemDAO(DaoTest):
    item_dao: ItemDAO

    def init_dao(self):
        self.item_dao = ItemDAO()

    def setup_method(self):
        pass

    def teardown_method(self):
        # Clean up any resources used by the tests here
        pass

    def test_get_items(self):
        items = self.item_dao.get_items()
        assert items != 0

    def test_create_item(self, any_item_create: ItemCreate):
        item = self.item_dao.create_item(any_item_create)
        assert item is not None
        assert item.id is not None
        assert item.name == any_item_create.name

    def test_update_item(self, persisted_item: Item):
        item_update = ItemUpdate(id=persisted_item.id, name="Updated Name")
        updated_item = self.item_dao.update_item(item_update)
        assert updated_item is not None
        assert updated_item.id == persisted_item.id
        assert updated_item.name == item_update.name

    def test_delete_item(self, any_item: Item):
        item = self.item_dao.create_item(any_item)
        item_created = self.item_dao.get_item_by_id(item.id)
        assert item_created is not None

        self.item_dao.delete_item(item.id)
        item_deleted = self.item_dao.get_item_by_id(item.id)
        assert item_deleted is None

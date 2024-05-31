from app.db.dao.item_dao import ItemDAO
from app.tests.dao_test import DaoTest

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
import logging
from typing import List

from fastapi import APIRouter, status

from app.db.service.item_service import ItemService
from app.entities.item import Item

ITEMS_PATH = "/items/"

ItemRouter = APIRouter()


@ItemRouter.get(
    ITEMS_PATH,
    response_model=List[Item],
    status_code=status.HTTP_200_OK,
)
def get_items() -> List[Item]:
    try:
        item_service = ItemService()
        items = item_service.get_items()
        return items
    except Exception as error:
        logging.error("Error in get_items.", exc_info=error)
        raise error

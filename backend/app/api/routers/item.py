import logging
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.db.service.item_service import ItemService
from app.entities.item import Item, ItemCreate, ItemUpdate

ITEMS_PATH = "/items"
SINGLE_ITEM_PATH = "/items/{item_id}"

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


@ItemRouter.get(
    SINGLE_ITEM_PATH,
    response_model=Item,
    status_code=status.HTTP_200_OK,
)
def get_item_by_id(item_id: int) -> Item:
    try:
        item_service = ItemService()
        item = item_service.get_item_by_id(item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found",
            )
        return item
    except Exception as error:
        logging.error("Error in get_item_by_id.", exc_info=error)
        raise error


@ItemRouter.post(
    ITEMS_PATH,
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
)
def create_item(item: ItemCreate) -> Item:
    try:
        item_service = ItemService()
        item = item_service.create_item(item)
        return item
    except Exception as error:
        logging.error("Error in create_item.", exc_info=error)
        raise error


@ItemRouter.patch(
    SINGLE_ITEM_PATH,
    response_model=Item,
    status_code=status.HTTP_200_OK,
)
def update_item(item_id: int, item: ItemCreate) -> Item:
    try:
        item_service = ItemService()
        item_update = ItemUpdate(id=item_id, name=item.name)
        item_updated = item_service.update_item(item_update)
        return item_updated
    except Exception as error:
        logging.error("Error in update_item.", exc_info=error)
        raise error


@ItemRouter.delete(
    SINGLE_ITEM_PATH,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(item_id: int) -> None:
    try:
        item_service = ItemService()
        item_service.delete_item(item_id)
    except Exception as error:
        logging.error("Error in delete_item.", exc_info=error)
        raise error

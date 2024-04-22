import random

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.middleware import BaseMiddleware
from app.api.routers.item import ItemRouter

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Add more allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseMiddleware)

RootRouter = APIRouter()


@RootRouter.get("/")
def read_root():
    return "Hellow World!"


@RootRouter.get("/random")
def get_random():
    items = ["item1", "item2", "item3", "item4"]  # Replace with your list of items
    random_item = random.choice(items)
    return random_item


app.include_router(RootRouter)
app.include_router(ItemRouter)

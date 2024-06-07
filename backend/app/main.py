import logging
import random
from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.middleware import BaseMiddleware
from app.api.routers.item import ItemRouter

app = FastAPI()

cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers": "*",
}


@app.exception_handler(HTTPException)
def api_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        headers=cors_headers,
        status_code=exc.status_code,
        content={"type": "http_error", "message": exc.detail},
    )


@app.exception_handler(Exception)
def api_catch_all_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    uuid = uuid4()
    logging.exception(f"Uncaught exception with UUID: {uuid}")
    return JSONResponse(
        headers=cors_headers,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "type": "uncaught_error",
            "message": f"Please contact support with the following UUID: {uuid}",
        },
    )


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

import logging
import random
from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException, Request, status

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.middleware import BaseMiddleware, RequestInterceptorMiddleware
from app.api.routers.auth import router as AuthRouter
from app.api.routers.users import router as UsersRouter

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
# Add request interceptor for debugging (add this before BaseMiddleware)
app.add_middleware(RequestInterceptorMiddleware)
app.add_middleware(BaseMiddleware)

RootRouter = APIRouter()


@RootRouter.get("/")
def read_root():
    return {"message": "Hello World!", "status": "API is working"}


@RootRouter.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}


@RootRouter.get("/random")
def get_random():
    options = ["option1", "option2", "option3", "option4"]
    random_option = random.choice(options)
    return {"option": random_option}


app.include_router(RootRouter)
app.include_router(AuthRouter, prefix="/auth", tags=["Authentication"])
app.include_router(UsersRouter, prefix="/users", tags=["User Management"])

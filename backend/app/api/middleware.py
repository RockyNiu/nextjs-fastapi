from backend.app.db.database import database_context
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class BaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        with database_context():
            try:
                response = await call_next(request)
            except Exception as e:
                raise e

        return response

import json
import logging
import time
from typing import Callable, Awaitable, Any
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.database import database_context


class RequestInterceptorMiddleware(BaseHTTPMiddleware):
    """
    Middleware to intercept and log HTTP requests and responses for debugging.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        # Start timing
        start_time = time.time()
        request_id = str(uuid.uuid4())

        try:
            # Log request details
            await self._log_request(request, request_id)

            # Process request
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            # Log response details
            self._log_response(request, response, process_time, request_id)

            # Add custom headers
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id

            return response
        except Exception as e:
            # Log error and calculate processing time
            process_time = time.time() - start_time
            logging.error(f"❌ Error processing request {request_id}: {str(e)}")
            raise e

    async def _log_request(self, request: Request, request_id: str):
        """Log incoming request details."""
        request_data: dict[str, Any] = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client": f"{request.client.host}:{request.client.port}"
            if request.client
            else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown"),
        }

        # Log request body for POST/PUT/PATCH requests
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    # Try to parse JSON, otherwise log as string
                    try:
                        request_data["body"] = json.loads(body.decode())
                    except json.JSONDecodeError:
                        request_data["body"] = body.decode()
            except Exception as e:
                request_data["body_error"] = str(e)

        logging.info(f"🔄 Incoming Request: {json.dumps(request_data, indent=2)}")

    def _log_response(
        self, request: Request, response: Response, process_time: float, request_id: str
    ):
        """Log outgoing response details."""
        response_data: dict[str, Any] = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time": f"{process_time:.4f}s",
            "response_headers": dict(response.headers),
        }

        logging.info(f"✅ Response: {json.dumps(response_data, indent=2)}")


class BaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        with database_context():
            try:
                response = await call_next(request)
            except Exception as e:
                raise e

            return response

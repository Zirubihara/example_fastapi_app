"""
middleware.py

This module contains middleware functions for the FastAPI application.
Currently, it includes a function to add CORS (Cross-Origin Resource Sharing)
support to the app, allowing it to handle requests from different origins.
"""

from fastapi.middleware.cors import CORSMiddleware
import time
from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


# middleware to add cors to the app
def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        calls: int = 10,
        window: int = 60
    ) -> None:
        super().__init__(app)
        self.calls = calls
        self.window = window
        self.cache = {}

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        key = f"{request.client.host}:{request.url.path}"
        current_time = time.time()
        
        # Clean old entries
        self.cache = {
            k: v for k, v in self.cache.items()
            if current_time - v["start"] < self.window
        }
        
        if key in self.cache:
            if len(self.cache[key]["calls"]) >= self.calls:
                return Response(
                    content="Too many requests",
                    status_code=429
                )
            self.cache[key]["calls"].append(current_time)
        else:
            self.cache[key] = {
                "start": current_time,
                "calls": [current_time]
            }
        
        return await call_next(request)

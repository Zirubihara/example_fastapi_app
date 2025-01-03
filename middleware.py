"""
middleware.py

This module contains middleware functions for the FastAPI application.
Currently, it includes a function to add CORS (Cross-Origin Resource Sharing)
support to the app, allowing it to handle requests from different origins.
"""

from fastapi.middleware.cors import CORSMiddleware


# middleware to add cors to the app
def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

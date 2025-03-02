from fastapi import APIRouter

from app.api.v1.endpoints import health, odd_numbers, users, auth

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(
    odd_numbers.router, prefix="/odd-numbers", tags=["odd-numbers"]
)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"]) 
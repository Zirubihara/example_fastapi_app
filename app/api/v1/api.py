from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, odd_numbers, users

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(
    odd_numbers.router, prefix="/odd-numbers", tags=["odd-numbers"]
)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

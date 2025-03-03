from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, odd_numbers, users

api_router = APIRouter()

# Add routers with tags and descriptions
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
    responses={404: {"description": "Not found"}},
)

api_router.include_router(
    odd_numbers.router,
    prefix="/odd-numbers",
    tags=["Odd Numbers"],
    responses={404: {"description": "Not found"}},
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

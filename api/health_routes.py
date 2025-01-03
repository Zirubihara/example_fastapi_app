from fastapi import APIRouter
from fastapi.responses import JSONResponse

from timing_decorator import time_logger

router = APIRouter()


@router.get("/health", response_model=dict[str, str])
@time_logger
async def health_check():
    """Health check endpoint to verify the application is running."""
    return JSONResponse(content={"status": "healthy"})

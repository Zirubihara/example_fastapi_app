from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from exceptions import HealthCheckError
from timing_decorator import time_logger

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=dict[str, str],
    summary="Health Check",
    status_code=status.HTTP_200_OK,
)
@time_logger
async def health_check():
    """
    Health check endpoint to verify the application is running.

    Returns:
        dict: Status information about the application

    Raises:
        HealthCheckError: If the health check fails
    """
    try:
        status_content = {"status": "healthy"}
        return JSONResponse(status_code=status.HTTP_200_OK, content=status_content)
    except Exception as e:
        raise HealthCheckError(f"Health check failed: {str(e)}")

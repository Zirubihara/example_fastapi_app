from .base import AppError


class HealthCheckError(AppError):
    """Exception raised when health check fails."""

    def __init__(self, message: str = "Health check failed"):
        super().__init__(message)

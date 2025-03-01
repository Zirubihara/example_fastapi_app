class AppError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str = "An unexpected error occurred"):
        super().__init__(message)
        self.message = message

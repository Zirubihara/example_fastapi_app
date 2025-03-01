from .base import AppError


class DatabaseError(AppError):
    """Base exception for all database-related errors."""

    def __init__(self, message: str = "A database error occurred"):
        super().__init__(message)


class IntegrityError(DatabaseError):
    """Exception for database integrity violations."""

    def __init__(self, message: str = "Database integrity violation"):
        super().__init__(message)


class ConnectionError(DatabaseError):
    """Exception for database connection issues."""

    def __init__(self, message: str = "Database connection error"):
        super().__init__(message)

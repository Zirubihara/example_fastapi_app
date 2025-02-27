from .base import AppError


class UserError(AppError):
    """Base exception for all user-related errors."""

    def __init__(self, message: str = "A user-related error occurred"):
        super().__init__(message)


class UserNotFoundError(UserError):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} not found")
        self.user_id = user_id


class UserValidationError(UserError):
    """Exception for user data validation errors."""

    def __init__(self, field: str, message: str):
        super().__init__(f"Validation error for {field}: {message}")
        self.field = field


class UserAlreadyExistsError(UserError):
    """Exception raised when attempting to create a duplicate user."""

    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists")
        self.email = email

class UserCreationError(Exception):
    """Base exception for errors during user creation."""

    def __init__(self, message: str = "An error occurred during user creation."):
        super().__init__(message)
        self.message = message


class UserIntegrityError(UserCreationError):
    """Exception raised for integrity constraint violations."""

    def __init__(
        self, message: str = "Integrity constraint violation during user creation."
    ):
        super().__init__(message)


class UserDatabaseError(UserCreationError):
    """Exception raised for database-related errors."""

    def __init__(self, message: str = "Database error occurred during user creation."):
        super().__init__(message)

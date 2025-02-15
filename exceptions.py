class UserCreationError(Exception):
    """Base exception for errors during user creation."""

    pass


class UserIntegrityError(UserCreationError):
    """Exception raised for integrity constraint violations."""

    pass


class UserDatabaseError(UserCreationError):
    """Exception raised for database-related errors."""

    pass

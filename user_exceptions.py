# user_exceptions.py


class UserError(Exception):
    """Base exception for errors related to user operations."""

    def __init__(self, message: str = "An error occurred with the user endpoint."):
        super().__init__(message)
        self.message = message


class UserNotFoundError(UserError):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: int, message: str = None):
        if message is None:
            message = f"User with ID {user_id} not found."
        super().__init__(message)


class UserDatabaseError(UserError):
    """Exception raised for errors during user database operations."""

    def __init__(self, message: str = None):
        if message is None:
            message = "Internal server error while retrieving users."
        super().__init__(message)

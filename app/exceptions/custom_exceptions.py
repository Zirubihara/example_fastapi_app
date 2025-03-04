from fastapi import HTTPException, status


class UserError(HTTPException):
    """Base exception for errors related to user operations."""

    def __init__(self, message: str = "An error occurred with the user endpoint."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )


class UserNotFoundError(HTTPException):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )


class UserDatabaseError(HTTPException):
    """Exception raised for errors during user database operations."""

    def __init__(self, message: str = "Internal server error while retrieving users."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )

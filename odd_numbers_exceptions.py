# odd_numbers_exceptions.py


class OddNumbersError(Exception):
    """Base exception for errors related to odd numbers endpoint."""

    def __init__(self, message: str = "An error occurred in the odd numbers endpoint."):
        super().__init__(message)
        self.message = message


class InvalidRangeError(OddNumbersError):
    """Exception raised when the start is greater than the end."""

    def __init__(self, message: str = None):
        if message is None:
            message = "The start must be less than or equal to the end."
        super().__init__(message)


class SumExceededError(OddNumbersError):
    """Exception raised when the sum of odd numbers exceeds the allowed limit."""

    def __init__(self, message: str = None):
        if message is None:
            message = "The sum of odd numbers exceeds the allowed limit."
        super().__init__(message)

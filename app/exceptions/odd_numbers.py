from .base import AppError


class OddNumbersError(AppError):
    """Base exception for odd numbers related errors."""

    def __init__(self, message: str = "An error occurred with odd numbers"):
        super().__init__(message)


class InvalidRangeError(OddNumbersError):
    """Exception raised when the range is invalid."""

    def __init__(self, start: int, end: int):
        super().__init__(f"Start ({start}) must be less than or equal to end ({end})")
        self.start = start
        self.end = end


class SumExceedsLimitError(OddNumbersError):
    """Exception raised when sum of odd numbers exceeds limit."""

    def __init__(self, sum_value: int, limit: int = 100):
        super().__init__(f"Sum of odd numbers ({sum_value}) exceeds limit of {limit}")
        self.sum_value = sum_value
        self.limit = limit

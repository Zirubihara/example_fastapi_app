from typing import List

from pydantic import BaseModel, ConfigDict, field_validator


class OddNumbersResponse(BaseModel):
    """
    Response model for odd numbers.

    This model represents a response containing a list of odd numbers.
    It validates that all numbers are odd and their sum doesn't exceed 100.

    Attributes:
        odd_numbers (List[int]): A list of odd integers
    """

    odd_numbers: List[int]

    model_config = ConfigDict(
        title="Odd Numbers Response Model",
        description="Response model for odd numbers.",
        json_schema_extra={"example": {"odd_numbers": [1, 3, 5, 7, 9]}},
    )

    @field_validator("odd_numbers", mode="before")
    @classmethod
    def validate_odd_numbers(cls, v: List[int]) -> List[int]:
        """
        Validate that the list contains at least one odd number.

        Args:
            v (List[int]): List of numbers to validate

        Returns:
            List[int]: Validated list of odd numbers

        Raises:
            ValueError: If list is empty or contains even numbers
        """
        if not v:
            raise ValueError("At least one number must be provided")

        if any(num % 2 == 0 for num in v):
            raise ValueError("All numbers must be odd")

        return v

    @field_validator("odd_numbers", mode="after")
    @classmethod
    def validate_sum_under_limit(cls, v: List[int]) -> List[int]:
        """
        Validate that the sum of odd numbers doesn't exceed 100.

        Args:
            v (List[int]): List of numbers to validate

        Returns:
            List[int]: Validated list of odd numbers

        Raises:
            ValueError: If sum exceeds 100
        """
        numbers_sum = sum(v)
        if numbers_sum > 100:
            raise ValueError(f"Sum of numbers ({numbers_sum}) must not exceed 100")

        return v

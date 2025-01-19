from typing import List, Sequence

from pydantic import BaseModel, ConfigDict, field_validator


class OddNumbersResponse(BaseModel):
    """Response model for odd numbers.

    This model represents a response containing a list of odd numbers.
    It validates that all numbers are odd and their sum doesn't exceed 100.

    Attributes:
        odd_numbers: A list of odd integers
    """

    odd_numbers: list[int]

    model_config = ConfigDict(
        title="Odd Numbers Response Model",
        description="Response model for odd numbers.",
        json_schema_extra={"example": {"odd_numbers": [1, 3, 5, 7, 9]}},
    )

    @field_validator("odd_numbers", mode="before")
    @classmethod
    def validate_odd_numbers(cls, values: Sequence[int]) -> list[int]:
        """Validate that the list contains only odd numbers.

        Args:
            values: List of numbers to validate

        Returns:
            The validated list of odd numbers

        Raises:
            ValueError: If list is empty or contains even numbers
        """
        if not values:
            raise ValueError("At least one number must be provided")

        even_numbers = [num for num in values if num % 2 == 0]
        if even_numbers:
            raise ValueError(
                f"All numbers must be odd. Found even numbers: {even_numbers}"
            )

        return list(values)

    @field_validator("odd_numbers", mode="after")
    @classmethod
    def validate_sum_under_limit(
        cls, values: Sequence[int], *, limit: int = 100
    ) -> list[int]:
        """Validate that the sum of odd numbers doesn't exceed the limit.

        Args:
            values: List of numbers to validate
            limit: Maximum allowed sum (defaults to 100)

        Returns:
            The validated list of odd numbers

        Raises:
            ValueError: If sum exceeds the limit
        """
        numbers_sum = sum(values)
        if numbers_sum > limit:
            raise ValueError(f"Sum of numbers ({numbers_sum}) must not exceed {limit}")

        return list(values)

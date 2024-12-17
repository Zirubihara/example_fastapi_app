from pydantic import BaseModel, field_validator
from typing import List


class OddNumbersResponse(BaseModel):
    """
    Response model for odd numbers.

    This model is used to represent a response containing a list of odd numbers.
    It includes validation to ensure that the list contains only odd numbers
    and that the sum of the numbers does not exceed a specified limit.

    Attributes:
        odd_numbers (List[int]): A list of odd integers.
    """

    odd_numbers: List[int]

    @field_validator("odd_numbers", mode="before")
    def validate_odd_numbers(cls, v):
        """
        Validate that the list contains at least one number and that all numbers are odd.

        Args:
            cls: The class being validated.
            v (List[int]): The value of the odd_numbers field.

        Raises:
            ValueError: If the list is empty or contains any even numbers.

        Returns:
            List[int]: The validated list of odd numbers.
        """
        if len(v) < 1:
            raise ValueError("At least one number must be provided")
        for number in v:
            if number % 2 == 0:
                raise ValueError("All numbers must be odd")
        return v

    @field_validator("odd_numbers", mode="after")
    def validate_sum_under_limit(cls, v):
        """
        Validate that the sum of the odd numbers does not exceed 100.

        Args:
            cls: The class being validated.
            v (List[int]): The value of the odd_numbers field.

        Raises:
            ValueError: If the sum of the numbers exceeds 100.

        Returns:
            List[int]: The validated list of odd numbers.
        """
        if sum(v) > 100:
            raise ValueError("Sum of numbers must not exceed 100")
        return v

    class Config:
        title = "Odd Numbers Response Model"
        description = "Response model for odd numbers."
        json_schema_extra = {"example": {"odd_numbers": [1, 3, 5, 7, 9]}}  # Updated key
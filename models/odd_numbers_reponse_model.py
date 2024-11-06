# models/odd_numbers_reponse_model.py
from pydantic import BaseModel, field_validator
from typing import List


class OddNumbersResponse(BaseModel):
    odd_numbers: List[int]

    @field_validator("odd_numbers", mode="before")
    def validate_odd_numbers(cls, v):
        if len(v) < 1:
            raise ValueError("At least one number must be provided")
        for number in v:
            if number % 2 == 0:
                raise ValueError("All numbers must be odd")
        return v

    @field_validator("odd_numbers", mode="after")
    def validate_sum_under_limit(cls, v):
        if sum(v) > 100:
            raise ValueError("Sum of numbers must not exceed 100")
        return v

    class Config:
        title = "Odd Numbers Response Model"
        description = "Response model for odd numbers."
        schema_extra = {"example": {"odd_numbers": [1, 3, 5, 7, 9]}}
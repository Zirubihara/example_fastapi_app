from pydantic import BaseModel, conlist, field_validator
from typing import Annotated, List

class OddNumbersResponse(BaseModel):
    odd_numbers: Annotated[List[int], conlist(int, min_items=1)]
    
    @field_validator('odd_numbers', mode='before')
    def validate_odd_numbers(cls, v):
        for number in v:
            if number % 2 == 0:
                raise ValueError('All numbers must be odd')
        return v
    
    @field_validator('odd_numbers', mode='after')
    def validate_sum_under_limit(cls, v):
        if sum(v) > 100:
            raise ValueError("Sum of numbers must not exceed 100")
        return v

    class Config:
        title = "Odd Numbers Response Model"
        description = "Response model for odd numbers."
        schema_extra = {
            "example": {
                "odd_numbers": [1, 3, 5, 7, 9]
            }
        }

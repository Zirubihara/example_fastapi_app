from pydantic import BaseModel
from typing import List

class OddNumbersResponse(BaseModel):
    odd_numbers: List[int]

    class Config:
        title = "Odd Numbers Response Model"
        description = "Response model for odd numbers."
        schema_extra = {
            "example": {
                "odd_numbers": [1, 3, 5, 7, 9]
            }
        }

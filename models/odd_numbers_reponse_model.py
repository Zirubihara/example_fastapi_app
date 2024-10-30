from pydantic import BaseModel
from typing import List

class OddNumbersResponse(BaseModel):
    odd_numbers: List[int]

    class Config:
        title = "Odd Numbers Response Model"
        description = "Response model for odd numbers."

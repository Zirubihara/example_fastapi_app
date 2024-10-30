from pydantic import BaseModel
from typing import List

class OddNumbersResponse(BaseModel):
    odd_numbers: List[int]
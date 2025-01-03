from fastapi import APIRouter, HTTPException

from logger import logger
from schemas.odd_numbers_reponse_model import OddNumbersResponse
from timing_decorator import time_logger

router = APIRouter()


@router.get("/odd-numbers/", response_model=OddNumbersResponse, status_code=200)
@time_logger
async def get_odd_numbers(start: int, end: int) -> OddNumbersResponse:
    """Returns odd numbers in the specified range."""
    logger.info(f"Fetching odd numbers from {start} to {end}.")
    if start > end:
        logger.error("Start must be greater than end.")
        raise HTTPException(
            status_code=400, detail="Start must be less than or equal to end."
        )

    numbers = list(range(start, end + 1))
    odd_numbers = [num for num in numbers if num % 2 != 0]

    if sum(odd_numbers) > 100:
        logger.error("Sum of odd numbers exceeds 100.")
        raise HTTPException(
            status_code=400, detail="Sum of odd numbers must not exceed 100."
        )

    return OddNumbersResponse(odd_numbers=odd_numbers)

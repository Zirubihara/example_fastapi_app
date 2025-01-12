from fastapi import APIRouter, HTTPException, status

from logger import logger
from schemas.odd_numbers_reponse_model import OddNumbersResponse
from timing_decorator import time_logger

router = APIRouter(tags=["Odd Numbers"])


@router.get(
    "/odd-numbers/",
    response_model=OddNumbersResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Odd Numbers",
    description="Returns odd numbers in the specified range with sum less than 100",
)
@time_logger
async def get_odd_numbers(start: int, end: int) -> OddNumbersResponse:
    """
    Returns odd numbers in the specified range.

    Args:
        start (int): Starting number of the range
        end (int): Ending number of the range

    Returns:
        OddNumbersResponse: List of odd numbers in the specified range

    Raises:
        HTTPException: If start > end or if sum of odd numbers > 100
    """
    logger.info(f"Fetching odd numbers from {start} to {end}")

    if start > end:
        error_msg = f"Start ({start}) must be less than or equal to end ({end})"
        logger.error(error_msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

    odd_numbers = [num for num in range(start, end + 1) if num % 2 != 0]
    numbers_sum = sum(odd_numbers)

    if numbers_sum > 100:
        error_msg = f"Sum of odd numbers ({numbers_sum}) exceeds 100"
        logger.error(error_msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

    logger.info(f"Found {len(odd_numbers)} odd numbers with sum {numbers_sum}")
    return OddNumbersResponse(odd_numbers=odd_numbers)

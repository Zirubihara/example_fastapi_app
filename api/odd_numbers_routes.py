from fastapi import APIRouter, status

from exceptions import InvalidRangeError, SumExceedsLimitError
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
        InvalidRangeError: If start > end
        SumExceedsLimitError: If sum of odd numbers > 100
    """
    logger.info(f"Fetching odd numbers from {start} to {end}")

    if start > end:
        logger.error(f"Invalid range: start ({start}) > end ({end})")
        raise InvalidRangeError(start, end)

    odd_numbers = [num for num in range(start, end + 1) if num % 2 != 0]
    numbers_sum = sum(odd_numbers)

    if numbers_sum > 100:
        logger.error(f"Sum ({numbers_sum}) exceeds limit of 100")
        raise SumExceedsLimitError(numbers_sum)

    logger.info(f"Found {len(odd_numbers)} odd numbers with sum {numbers_sum}")
    return OddNumbersResponse(odd_numbers=odd_numbers)

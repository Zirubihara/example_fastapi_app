from fastapi import APIRouter, status, Path

from app.exceptions import InvalidRangeError, SumExceedsLimitError
from app.schemas.responses.odd_numbers import OddNumbersResponse
from app.utils.timing_decorator import time_logger
from app.core.logger import logger

router = APIRouter()


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


@router.get("/check/{number}")
async def check_odd_number(
    number: int = Path(..., description="Number to check")
):
    return {"number": number, "is_odd": number % 2 != 0}

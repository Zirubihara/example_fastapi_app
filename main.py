from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from config import Config
from database import Base  # Ensure you have the correct path to the database file
from logger import logger  # Import logger
from middleware import add_cors_middleware
from api.user_routes import router as user_router  # Import the user router
from schemas.odd_numbers_reponse_model import (
    OddNumbersResponse,
)  # Updated import for Pydantic model
from timing_decorator import time_logger  # Import timing decorator

# Create engine using the configuration
engine = create_engine(Config.DATABASE_URL)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
add_cors_middleware(app)

# Include the user router
app.include_router(user_router)


@app.get("/health", response_model=dict[str, str])
@time_logger
async def health_check():
    """Health check endpoint to verify the application is running.

    This endpoint returns a JSON response indicating the health status.
    Note: Using JSONResponse is optional; returning a dictionary would
    yield the same result as FastAPI automatically converts it to JSON.
    """
    return JSONResponse(content={"status": "healthy"})


@app.get("/odd-numbers/", response_model=OddNumbersResponse, status_code=200)
@time_logger
async def get_odd_numbers(start: int, end: int) -> OddNumbersResponse:
    """Returns odd numbers in the specified range."""
    logger.info(f"Fetching odd numbers from {start} to {end}.")  # Logging information
    if start > end:
        logger.error("Start must be greater than end.")  # Logging error
        raise HTTPException(
            status_code=400, detail="Start must be less than or equal to end."
        )

    numbers = list(range(start, end + 1))
    odd_numbers = [num for num in numbers if num % 2 != 0]

    # Check if the sum of numbers does not exceed 100
    if sum(odd_numbers) > 100:
        logger.error("Sum of odd numbers exceeds 100.")  # Logging error
        raise HTTPException(
            status_code=400, detail="Sum of odd numbers must not exceed 100."
        )

    return OddNumbersResponse(odd_numbers=odd_numbers)

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from middleware import add_cors_middleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import (
    SessionLocal,
    Base,
)  # Ensure you have the correct path to the database file
from logger import logger  # Import logger
from models.user import User  # Updated import for SQLAlchemy model
from schemas.user_response_model import (
    UserResponse,
)  # Updated import for Pydantic model
from schemas.odd_numbers_reponse_model import (
    OddNumbersResponse,
)  # Updated import for Pydantic model
from config import Config  # Importuj klasę Config


# Create engine using the configuration
engine = create_engine(Config.DATABASE_URL)


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

add_cors_middleware(app)


@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(name: str, email: str):
    db = SessionLocal()
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    logger.info(f"Created user with ID: {user.id}")  # Logging information
    return UserResponse(user_id=user.id, name=user.name, email=user.email)


@app.get("/users/", response_model=list[UserResponse], status_code=200)
async def get_users():
    """Returns a list of users."""
    db: Session = SessionLocal()
    users = db.query(User).all()  # Retrieve all users
    db.close()
    return [
        UserResponse(user_id=user.id, name=user.name, email=user.email)
        for user in users
    ]


@app.get("/users/{user_id}", response_model=UserResponse, status_code=200)
async def get_user(user_id: int):
    """Returns a user by ID."""
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()  # Retrieve user by ID
    db.close()
    if user is None:
        logger.error(f"User with ID {user_id} not found.")  # Logging error
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(user_id=user.id, name=user.name, email=user.email)


@app.get("/odd-numbers/", response_model=OddNumbersResponse, status_code=200)
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

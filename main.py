from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine

from database import SessionLocal, engine
from logger import logger  # Import loggera
from models.odd_numbers_reponse_model import OddNumbersResponse
from models.user import User
from models.user_model import User
from models.user_response_model import UserResponse

User.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users/")
async def create_user(name: str, email: str):
    db = SessionLocal()
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: User) -> UserResponse:
    """Creates a new user."""
    logger.info(f"Creating user with ID: {user.id}")  # Logowanie informacji
    if user.id <= 0:  # Przykład: nieprawidłowy identyfikator
        logger.error("Invalid user ID provided.")  # Logowanie błędu
        raise HTTPException(status_code=400, detail="Invalid user ID.")

    return UserResponse(user_id=user.id, name=user.name, email=user.email)


@app.get("/odd-numbers/", response_model=OddNumbersResponse, status_code=200)
async def get_odd_numbers(start: int, end: int) -> OddNumbersResponse:
    """Returns odd numbers in the specified range."""
    logger.info(f"Fetching odd numbers from {start} to {end}.")  # Logowanie informacji
    if start > end:
        logger.error("Start must be greater than end.")  # Logowanie błędu
        raise HTTPException(
            status_code=400, detail="Start must be less than or equal to end."
        )

    numbers = list(range(start, end + 1))
    odd_numbers = numbers[slice(1, None, 2)]
    return OddNumbersResponse(odd_numbers=odd_numbers)

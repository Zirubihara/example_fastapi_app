from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from database import SessionLocal, Base  # Upewnij się, że importujesz Base
from logger import logger  # Import loggera
from schemas.odd_numbers_reponse_model import OddNumbersResponse
from models.user import User
from schemas.user_response_model import UserResponse
from sqlalchemy.orm import Session

# Ustawienia bazy danych
DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydatabase"  # Zaktualizuj zgodnie z Twoimi danymi
engine = create_engine(DATABASE_URL)

# Tworzenie tabel
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(name: str, email: str):
    db = SessionLocal()
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    logger.info(f"Created user with ID: {user.id}")  # Logowanie informacji
    return UserResponse(user_id=user.id, name=user.name, email=user.email)


@app.get("/users/", response_model=list[UserResponse], status_code=200)
async def get_users():
    """Returns a list of users."""
    db: Session = SessionLocal()
    users = db.query(User).all()  # Pobierz wszystkich użytkowników
    db.close()
    return [
        UserResponse(user_id=user.id, name=user.name, email=user.email)
        for user in users
    ]


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

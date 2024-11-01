from fastapi import FastAPI, HTTPException

from models.odd_numbers_reponse_model import OddNumbersResponse
from models.user_model import User
from models.user_response_model import UserResponse

app = FastAPI()


@app.get("/")
async def read_root() -> dict:
    return {"message": "Witaj w FastAPI!"}


@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: User) -> UserResponse:
    # Przykładowa logika do sprawdzenia, czy użytkownik już istnieje
    if user.id <= 0:  # Przykład: nieprawidłowy identyfikator
        raise HTTPException(status_code=400, detail="Invalid user ID.")

    # Możesz dodać więcej logiki do tworzenia użytkownika
    # Na przykład, jeśli użytkownik już istnieje:
    # if user_exists(user.id):
    #     raise HTTPException(status_code=409, detail="User already exists.")

    return UserResponse(user_id=user.id, name=user.name, email=user.email)


@app.get("/odd-numbers/", response_model=OddNumbersResponse, status_code=200)
async def get_odd_numbers(start: int, end: int) -> OddNumbersResponse:
    if start > end:
        raise HTTPException(
            status_code=400, detail="Start must be less than or equal to end."
        )

    numbers = list(range(start, end + 1))
    odd_numbers = numbers[slice(1, None, 2)]
    return OddNumbersResponse(odd_numbers=odd_numbers)

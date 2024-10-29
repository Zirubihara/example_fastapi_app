# main.py
from fastapi import FastAPI

from models.user_model import User

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Witaj w FastAPI!"}

@app.post("/users/")
async def create_user(user: User):
    return {"user_id": user.id, "name": user.name, "email": user.email}
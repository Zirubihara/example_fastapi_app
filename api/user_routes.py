from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import (
    SessionLocal,
)  # Ensure you have the correct path to your database file
from models.user import User
from schemas.user_response_model import UserResponse  # Import your response model
from logger import logger  # Import logger

router = APIRouter()


# Example GET endpoint to retrieve users (you can modify this as needed)
@router.get("/users/", response_model=List[UserResponse])
async def get_users():
    """Retrieve a list of users."""
    db: Session = SessionLocal()
    try:
        # Logic to retrieve users from the database
        users = db.query(User).all()  # Replace with your actual query
        return [
            UserResponse(user_id=user.id, name=user.name, email=user.email)
            for user in users
        ]
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()


# Example GET endpoint to retrieve a user by ID
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Retrieve a user by ID."""
    db: Session = SessionLocal()
    try:
        user = (
            db.query(User).filter(User.id == user_id).first()
        )  # Replace with your actual query
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(user_id=user.id, name=user.name, email=user.email)
    except Exception as e:
        logger.error(f"Error retrieving user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()

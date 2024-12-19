from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import (
    SessionLocal,
)  # Ensure you have the correct path to your database file
from models.user import User
from schemas.user_response_model import UserResponse  # Import your response model
from logger import logger  # Import logger
from typing import List  # Import List for response model annotation

router = APIRouter()


# Example GET endpoint to retrieve users (you can modify this as needed)
@router.get("/users/", response_model=List[UserResponse])
async def get_users():
    """
    Retrieve a list of all users from the database.

    This endpoint fetches all user records from the database and returns them
    as a list of `UserResponse` objects. If an error occurs during the query,
    a 500 Internal Server Error is raised.

    Returns:
        List[UserResponse]: A list of users containing their ID, name, and email.

    Raises:
        HTTPException: If there is an error during database access or query execution.
    """
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
    """
    Retrieve a specific user by their ID.

    This endpoint fetches a single user record from the database based on the
    provided `user_id`. If the user is not found, a 404 Not Found error is raised.
    Any other error results in a 500 Internal Server Error.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        UserResponse: The user details containing their ID, name, and email.

    Raises:
        HTTPException: If the user is not found or there is an error during
        database access or query execution.
    """
    db: Session = SessionLocal()
    try:
        # Query the database for the user with the given ID
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(user_id=user.id, name=user.name, email=user.email)
    except Exception as e:
        logger.error(f"Error retrieving user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()

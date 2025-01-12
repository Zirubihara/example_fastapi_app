from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
from logger import logger
from models.user import User
from schemas.user_response_model import UserResponse

router = APIRouter(tags=["Users"])


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/users/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get All Users",
)
async def get_users(db: Session = Depends(get_db)):
    """
    Retrieve a list of all users from the database.

    This endpoint fetches all user records from the database and returns them
    as a list of UserResponse objects.

    Returns:
        List[UserResponse]: A list of users containing their ID, name, and email.

    Raises:
        HTTPException: If there is an error during database access or query execution.
    """
    try:
        logger.info("Fetching all users from database")
        users = db.query(User).all()
        logger.info(f"Successfully retrieved {len(users)} users")

        return [
            UserResponse(user_id=user.id, name=user.name, email=user.email)
            for user in users
        ]
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving users",
        )


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get User by ID",
)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve
        db (Session): Database session dependency

    Returns:
        UserResponse: The user details containing their ID, name, and email

    Raises:
        HTTPException: If the user is not found (404) or there is a server error (500)
    """
    try:
        logger.info(f"Attempting to fetch user with ID: {user_id}")
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )

        logger.info(f"Successfully retrieved user with ID: {user_id}")
        return UserResponse(user_id=user.id, name=user.name, email=user.email)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving user",
        )

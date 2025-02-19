from typing import List

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import SessionLocal
from logger import logger
from models.user import User
from schemas.user_response_model import UserResponse
from user_exceptions import UserDatabaseError, UserNotFoundError

router = APIRouter(tags=["Users"])


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Exception Handlers
@router.exception_handler(UserNotFoundError)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@router.exception_handler(UserDatabaseError)
async def user_database_exception_handler(request: Request, exc: UserDatabaseError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message},
    )


@router.get(
    "/users/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get All Users",
)
async def get_users(db: Session = Depends(get_db)):
    """
    Retrieve a list of all users from the database.

    Returns:
        List[UserResponse]: A list of users containing their ID, name, surname, and email.

    Raises:
        UserDatabaseError: If there is an error during database access.
    """
    try:
        logger.info("Fetching all users from database")
        users = db.query(User).all()
        logger.info(f"Successfully retrieved {len(users)} users")

        return [
            UserResponse(
                user_id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
            )
            for user in users
        ]
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise UserDatabaseError() from e


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
        user_id (int): The ID of the user to retrieve.

    Returns:
        UserResponse: The user details containing their ID, name, surname, and email.

    Raises:
        UserNotFoundError: If the user is not found.
        UserDatabaseError: If there is an error during the database operation.
    """
    try:
        logger.info(f"Attempting to fetch user with ID: {user_id}")
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            logger.warning(f"User with ID {user_id} not found")
            raise UserNotFoundError(user_id)

        logger.info(f"Successfully retrieved user with ID: {user_id}")
        return UserResponse(
            user_id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
        )

    except UserNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user with ID {user_id}: {str(e)}")
        raise UserDatabaseError() from e

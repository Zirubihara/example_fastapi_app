from typing import List

from fastapi import APIRouter, Depends, Request, status, Security
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logger import logger
from app.exceptions import UserDatabaseError, UserNotFoundError
from app.models.user import User
from app.schemas.responses.user import UserResponse
from app.schemas.requests.user import UserCreate
from app.services.users import create_user
from app.utils.timing_decorator import time_logger
from app.api.deps import get_current_admin_user, get_current_active_user
from app.schemas.user import UserUpdate

router = APIRouter(tags=["Users"])


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


@router.post(
    "/users/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
)
@time_logger
async def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Create a new user.

    Args:
        user: User data
        db: Database session

    Returns:
        UserResponse: Created user data
    """
    return create_user(db=db, name=user.name, surname=user.surname, email=user.email)


@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Get current user."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Update current user."""
    user = current_user
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=List[UserResponse])
async def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Security(get_current_admin_user),
) -> List[User]:
    """Get all users. Admin only."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

from typing import List

from fastapi import APIRouter, Depends, status, Security, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logger import logger
from app.exceptions import UserDatabaseError, UserNotFoundError
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.crud import crud_user
from app.api.deps import get_current_admin_user, get_current_active_user
from app.utils.timing_decorator import time_logger

router = APIRouter(tags=["Users"])


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get All Users",
)
@time_logger
async def get_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Security(get_current_admin_user),
) -> List[UserResponse]:
    """
    Retrieve a list of all users from the database. Admin only.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current admin user

    Returns:
        List[UserResponse]: A list of users containing their ID, name, surname,
        and email.

    Raises:
        UserDatabaseError: If there is an error during database access.
    """
    try:
        logger.info("Fetching users from database")
        users = crud_user.get_multi(db, skip=skip, limit=limit)
        logger.info(f"Successfully retrieved {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise UserDatabaseError() from e


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get User by ID",
)
@time_logger
async def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """
    Retrieve a specific user by their ID.

    Args:
        user_id: The ID of the user to retrieve
        db: Database session

    Returns:
        UserResponse: The user details containing their ID, name, surname, and email.

    Raises:
        UserNotFoundError: If the user is not found.
        UserDatabaseError: If there is an error during the database operation.
    """
    try:
        logger.info(f"Attempting to fetch user with ID: {user_id}")
        user = crud_user.get(db, id=user_id)

        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise UserNotFoundError(user_id)

        logger.info(f"Successfully retrieved user with ID: {user_id}")
        return user

    except UserNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user with ID {user_id}: {str(e)}")
        raise UserDatabaseError() from e


@router.post(
    "/",
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

    Raises:
        HTTPException: If email is already registered
    """
    existing_user = crud_user.get_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud_user.create(db, obj_in=user)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get Current User",
)
@time_logger
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """
    Get current user.

    Args:
        current_user: Current authenticated user

    Returns:
        UserResponse: Current user data
    """
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update Current User",
)
@time_logger
async def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """
    Update current user.

    Args:
        db: Database session
        user_in: User update data
        current_user: Current authenticated user

    Returns:
        UserResponse: Updated user data
    """
    return crud_user.update(db, db_obj=current_user, obj_in=user_in)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update User",
)
@time_logger
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_admin_user),
) -> UserResponse:
    """
    Update user. Admin only.

    Args:
        user_id: ID of the user to update
        user_in: User update data
        db: Database session
        current_user: Current admin user

    Returns:
        UserResponse: Updated user data

    Raises:
        HTTPException: If user is not found
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return crud_user.update(db, db_obj=user, obj_in=user_in)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete User",
)
@time_logger
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_admin_user),
) -> None:
    """
    Delete user. Admin only.

    Args:
        user_id: ID of the user to delete
        db: Database session
        current_user: Current admin user

    Raises:
        HTTPException: If user is not found
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    crud_user.remove(db, id=user_id)

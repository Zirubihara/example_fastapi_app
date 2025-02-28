import re

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from exceptions.base import AppError
from exceptions.database import DatabaseError
from exceptions.user import UserAlreadyExistsError, UserValidationError
from logger import logger
from models.user import User

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def _validate_user_data(name: str, surname: str, email: str) -> None:
    """
    Validate user input data.

    Args:
        name (str): User's first name
        surname (str): User's surname
        email (str): User's email address

    Raises:
        UserValidationError: If any of the input data is invalid
    """
    if not name or not name.isalpha():
        raise UserValidationError("name", "Must contain only letters")
    if not surname or not surname.isalpha():
        raise UserValidationError("surname", "Must contain only letters")
    if not email or not re.match(EMAIL_PATTERN, email):
        raise UserValidationError("email", "Invalid email format")


def create_user(db: Session, name: str, surname: str, email: str) -> User | None:
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        name (str): User's first name.
        surname (str): User's surname.
        email (str): User's email address.

    Returns:
        User | None: The created user object or None if creation fails.

    Raises:
        UserValidationError: If input data is invalid.
        UserAlreadyExistsError: If user with email already exists.
        DatabaseError: If there is a database error.
    """
    try:
        _validate_user_data(name, surname, email)

        user = User(name=name, surname=surname, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(f"User created successfully with ID: {user.id}")
        return user

    except SQLAlchemyError as e:
        db.rollback()
        if "unique constraint" in str(e).lower():
            logger.warning(f"Attempt to create duplicate user with email: {email}")
            raise UserAlreadyExistsError(email)
        logger.error(f"Database error while creating user: {str(e)}")
        raise DatabaseError("Failed to create user") from e

    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating user: {str(e)}")
        raise AppError(f"Failed to create user: {str(e)}") from e

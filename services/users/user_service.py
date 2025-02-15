from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from exceptions import UserCreationError, UserDatabaseError, UserIntegrityError
from logger import logger
from models.user import User


def create_user(db: Session, name: str, surname: str, email: str) -> Optional[User]:
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        name (str): User's first name.
        surname (str): User's surname.
        email (str): User's email address.

    Returns:
        Optional[User]: The created user object or None if the creation failed.

    Raises:
        UserIntegrityError: If there is an integrity constraint violation.
        UserDatabaseError: If there is a database error.
        UserCreationError: If an unexpected error occurs.
    """
    try:
        logger.info(f"Attempting to create user with email: {email}")

        user = User(name=name, surname=surname, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(f"User created successfully with ID: {user.id}")
        return user

    except IntegrityError as e:
        db.rollback()
        logger.error(
            f"Integrity error while creating user with email {email}: {str(e)}"
        )
        raise UserIntegrityError(
            "Failed to create user due to an integrity constraint violation."
        ) from e

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while creating user: {str(e)}")
        raise UserDatabaseError("Failed to create user due to a database error.") from e

    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating user: {str(e)}")
        raise UserCreationError(
            "An unexpected error occurred during user creation."
        ) from e

from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from logger import logger
from models.user import User


def create_user(db: Session, name: str, surname: str, email: str) -> Optional[User]:
    """
    Create a new user in the database.

    Args:
        db (Session): Database session
        name (str): User's first name
        surname (str): User's surname
        email (str): User's email address

    Returns:
        Optional[User]: Created user object or None if creation failed

    Raises:
        SQLAlchemyError: If there's a database error
        IntegrityError: If there's a unique constraint violation
    """
    try:
        logger.info(f"Attempting to create user with email: {email}")

        user = User(name=name, surname=surname, email=email)

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(f"Successfully created user with ID: {user.id}")
        return user

    except IntegrityError as e:
        db.rollback()
        logger.error(
            f"Integrity error while creating user with email {email}: {str(e)}"
        )
        raise

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while creating user: {str(e)}")
        raise

    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating user: {str(e)}")
        raise

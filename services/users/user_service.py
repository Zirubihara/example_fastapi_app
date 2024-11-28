# services/user_service.py

from sqlalchemy.orm import Session
from models.user import User
import logging

logger = logging.getLogger(__name__)


def create_user(db: Session, name: str, email: str) -> User:
    """Create a new user in the database."""
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Created user with ID: {user.id}")  # Logging information
    return user

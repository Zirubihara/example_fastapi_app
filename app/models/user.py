from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    """
    User model representing a user in the system.
    This model defines the structure of the 'users' table in the database,
    including the user's ID, name, surname, and email address. It uses SQLAlchemy's
    ORM capabilities to map the class to the database table.

    Attributes:
        id (int): The unique identifier for the user (primary key).
        name (str): The name of the user (max length 100).
        surname (str): The surname of the user (max length 100).
        email (str): The email address of the user (must be unique).
        role (str): The role of the user (default USER).
        is_active (bool): Whether the user is active (default True).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

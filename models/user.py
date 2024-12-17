from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    """
    User model representing a user in the system.

    This model defines the structure of the 'users' table in the database,
    including the user's ID, name, and email address. It uses SQLAlchemy's
    ORM capabilities to map the class to the database table.

    Attributes:
        id (int): The unique identifier for the user (primary key).
        name (str): The name of the user.
        email (str): The email address of the user (must be unique).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
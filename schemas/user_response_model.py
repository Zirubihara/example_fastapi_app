from dataclasses import dataclass
from typing import Dict

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserResponse(BaseModel):
    """Response model for user data.

    This model represents the response returned when a user is created
    or retrieved from the system.

    Attributes:
        user_id: Unique identifier for the user
        name: User's first name
        surname: User's surname
        email: User's email address
    """

    user_id: int
    name: str
    surname: str
    email: EmailStr

    model_config = ConfigDict(
        title="User Response Model",
        description="Response model for user operations.",
        json_schema_extra={
            "example": {
                "user_id": 1,
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@example.com",
            }
        },
    )

    @property
    def full_name(self) -> str:
        """Get user's full name.

        Returns:
            The user's full name (name + surname)
        """
        return f"{self.name} {self.surname}"

    def to_public_dict(self) -> Dict[str, str | int]:
        """Convert user data to a dictionary, excluding sensitive information.

        Returns:
            A dictionary containing public user information
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
        }

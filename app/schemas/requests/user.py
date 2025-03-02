from typing import Any

from pydantic import (BaseModel, ConfigDict, EmailStr, field_validator,
                      model_validator)

from app.core.config import settings


class UserBase(BaseModel):
    """Base user model with common attributes.

    This model contains fields that are common between different user models
    (create, update, response).

    Attributes:
        name: User's first name
        surname: User's surname
        email: User's email address with domain validation
    """
    name: str
    surname: str
    email: EmailStr

    @field_validator("name", "surname")
    @classmethod
    def validate_name_length(cls, value: str, field: Any) -> str:
        """Validate name and surname length and format.

        Args:
            value: Name or surname to validate
            field: Field being validated

        Returns:
            The validated and properly capitalized name

        Raises:
            ValueError: If name is too short or contains non-letters
        """
        cleaned_value = value.strip()
        if len(cleaned_value) < 2:
            raise ValueError(f"{field.name} must be at least 2 characters long")
        if not cleaned_value.isalpha():
            raise ValueError(f"{field.name} must contain only letters")
        return cleaned_value.title()

    @field_validator("email")
    @classmethod
    def email_must_be_allowed_domain(cls, value: EmailStr) -> EmailStr:
        """Validate that the email domain is allowed.

        Args:
            value: Email address to validate

        Returns:
            The validated email address

        Raises:
            ValueError: If email domain is not in allowed list
        """
        if not value.endswith(settings.ALLOWED_EMAIL_DOMAIN):
            raise ValueError(
                f"Email must end with {settings.ALLOWED_EMAIL_DOMAIN}, got {value}"
            )
        return value


class UserCreate(UserBase):
    """User creation model.

    This model is used when creating a new user. It extends UserBase
    and adds password field.

    Attributes:
        password: User's password (will be hashed before storage)
    """
    password: str

    model_config = ConfigDict(
        title="User Creation Model",
        description="Model for creating new users.",
        json_schema_extra={
            "example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@gmail.com",
                "password": "strongpassword123",
            }
        },
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Validate password length and complexity.

        Args:
            value: Password to validate

        Returns:
            The validated password

        Raises:
            ValueError: If password is too short
        """
        if len(value) < settings.PASSWORD_MIN_LENGTH:
            raise ValueError(
                "Password must be at least "
                f"{settings.PASSWORD_MIN_LENGTH} characters long"
            )
        return value


class User(UserBase):
    """User model representing a user in the system.

    This model extends UserBase and adds an ID field. It's used for
    representing existing users in the system.

    Attributes:
        id: Unique identifier for the user
    """
    id: int

    model_config = ConfigDict(
        title="User Model",
        description="Model representing a user in the system.",
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@gmail.com",
            }
        },
    )

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int) -> int:
        """Validate user ID is positive.

        Args:
            value: ID to validate

        Returns:
            The validated ID

        Raises:
            ValueError: If ID is not positive
        """
        if value <= 0:
            raise ValueError("ID must be a positive integer")
        return value

    @model_validator(mode="after")
    def name_and_surname_must_be_different(self) -> "User":
        """Ensure that name and surname are different.

        Returns:
            The validated User instance

        Raises:
            ValueError: If name equals surname (case-insensitive)
        """
        if self.name.lower() == self.surname.lower():
            raise ValueError("Name and surname must not be the same")
        return self

from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, model_validator

from app.core.config import settings


class UserBase(BaseModel):
    """Base user model with common attributes.

    This model contains fields that are common between different user models
    (create, update, response).

    Attributes:
        name: User's first name
        surname: User's surname
        email: User's email address with domain validation
        is_active: Whether the user account is active
    """
    name: str
    surname: str
    email: EmailStr
    is_active: bool = True

    @field_validator("name", "surname")
    @classmethod
    def validate_name_length(cls, value: str) -> str:
        """Validate name and surname length and format.

        Args:
            value: Name or surname to validate

        Returns:
            The validated and properly capitalized name

        Raises:
            ValueError: If name is too short or contains non-letters
        """
        cleaned_value = value.strip()
        if len(cleaned_value) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if not cleaned_value.isalpha():
            raise ValueError("Name must contain only letters")
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


class UserUpdate(UserBase):
    """User update model.

    This model is used when updating an existing user. All fields are optional
    to allow partial updates.

    Attributes:
        name: Optional new name
        surname: Optional new surname
        email: Optional new email
        password: Optional new password
        is_active: Optional new active status
    """
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(
        title="User Update Model",
        description="Model for updating users.",
        json_schema_extra={
            "example": {
                "name": "John",
                "surname": "Smith",
                "email": "john.smith@gmail.com",
            }
        },
    )


class UserResponse(UserBase):
    """User response model.

    This model represents the response returned when a user is retrieved
    from the system.

    Attributes:
        id: Unique identifier for the user
        is_superuser: Whether the user has admin privileges
    """
    id: int
    is_superuser: bool = False

    model_config = ConfigDict(
        title="User Response Model",
        description="Response model for user operations.",
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@gmail.com",
                "is_active": True,
                "is_superuser": False,
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
    def name_and_surname_must_be_different(self) -> "UserResponse":
        """Ensure that name and surname are different.

        Returns:
            The validated User instance

        Raises:
            ValueError: If name equals surname (case-insensitive)
        """
        if self.name.lower() == self.surname.lower():
            raise ValueError("Name and surname must not be the same")
        return self 
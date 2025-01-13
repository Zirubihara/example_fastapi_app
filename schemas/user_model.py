from pydantic import (BaseModel, ConfigDict, EmailStr, field_validator,
                      model_validator)

from config import Config


class User(BaseModel):
    """
    User model representing a user in the system.

    This model validates and serializes user data, including ID, name,
    surname, and email address. It ensures the email domain is allowed
    and that name differs from surname.

    Attributes:
        id (int): Unique identifier for the user
        name (str): User's first name
        surname (str): User's surname
        email (EmailStr): User's email address with domain validation
    """

    id: int
    name: str
    surname: str
    email: EmailStr

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

    @field_validator("email")
    @classmethod
    def email_must_be_allowed_domain(cls, v: EmailStr) -> EmailStr:
        """
        Validate that the email domain is allowed.

        Args:
            v (EmailStr): Email address to validate

        Returns:
            EmailStr: Validated email address

        Raises:
            ValueError: If email domain is not allowed
        """
        if not v.endswith(Config.ALLOWED_EMAIL_DOMAIN):
            raise ValueError(
                f"Email must end with {Config.ALLOWED_EMAIL_DOMAIN}, got {v}"
            )
        return v

    @field_validator("name", "surname")
    @classmethod
    def validate_name_length(cls, v: str, field) -> str:
        """
        Validate name and surname length and format.

        Args:
            v (str): Name or surname to validate
            field: Field being validated

        Returns:
            str: Validated name or surname

        Raises:
            ValueError: If validation fails
        """
        if len(v.strip()) < 2:
            raise ValueError(f"{field.name} must be at least 2 characters long")
        if not v.isalpha():
            raise ValueError(f"{field.name} must contain only letters")
        return v.title()  # Capitalize first letter

    @model_validator(mode="after")
    def name_and_surname_must_be_different(self) -> "User":
        """
        Ensure that name and surname are different.

        Returns:
            User: Validated user model

        Raises:
            ValueError: If name equals surname
        """
        if self.name.lower() == self.surname.lower():
            raise ValueError("Name and surname must not be the same")
        return self

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: int) -> int:
        """
        Validate user ID.

        Args:
            v (int): ID to validate

        Returns:
            int: Validated ID

        Raises:
            ValueError: If ID is invalid
        """
        if v <= 0:
            raise ValueError("ID must be a positive integer")
        return v

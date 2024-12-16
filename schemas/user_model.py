from pydantic import BaseModel, EmailStr, field_validator, model_validator
from config import Config  # Import the Config class


class User(BaseModel):
    """
    User model representing a user in the system.

    This model is used to validate and serialize user data, including
    the user's ID, name, surname, and email address. It includes validation
    for the email domain and ensures that the name and surname are not the same.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The name of the user.
        surname (str): The surname of the user.
        email (EmailStr): The email address of the user, validated to ensure it
                          ends with the allowed domain.
    """

    id: int
    name: str
    surname: str
    email: EmailStr

    @field_validator("email")
    def email_must_be_allowed_domain(cls, v):
        """Validate that the email ends with the allowed domain."""
        if not v.endswith(Config.ALLOWED_EMAIL_DOMAIN):
            raise ValueError(
                f"Email must be an address ending with {Config.ALLOWED_EMAIL_DOMAIN}"
            )
        return v

    @model_validator(mode="after")
    def name_and_surname_must_be_different(cls, values):
        """Ensure that the name and surname are not the same."""
        if values.get("name") == values.get("surname"):
            raise ValueError("Name and surname must not be the same")
        return values

    class Config:
        title = "User Model"
        description = "Model representing a user in the system."
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@gmail.com",
            }
        }

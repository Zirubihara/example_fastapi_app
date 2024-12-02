from pydantic import BaseModel, EmailStr, field_validator, model_validator
from config import Config  # Import the Config class


class User(BaseModel):
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

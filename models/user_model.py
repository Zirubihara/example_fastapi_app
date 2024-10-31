# models.py
from pydantic import BaseModel, EmailStr, field_validator

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    @field_validator('email')
    def email_must_be_gmail(cls, v):
        if not v.endswith('@gmail.com'):
            raise ValueError('Email must be a Gmail address (ending with @gmail.com)')
        return v

    class Config:
        title = "User Model"
        description = "Model representing a user in the system."
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }


# models.py
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

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


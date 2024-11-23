from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str

    class Config:
        title = "User Response Model"
        description = "Response model for user creation."
        json_schema_extra = {  # Updated key
            "example": {
                "user_id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
            }
        }
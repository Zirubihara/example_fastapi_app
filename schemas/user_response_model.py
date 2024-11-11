from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    
    
    test: str

    class Config:
        title = "User Response Model"
        description = "Response model for user creation."
        schema_extra = {
            "example": {
                "user_id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
            }
        }

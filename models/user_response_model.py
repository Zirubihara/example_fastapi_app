from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str

    class Config:
        title = "User Response Model"
        description = "Response model for user creation."

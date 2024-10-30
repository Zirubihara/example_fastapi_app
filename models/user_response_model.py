from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
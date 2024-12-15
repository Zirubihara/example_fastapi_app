from pydantic import BaseModel


class UserResponse(BaseModel):
    """
    Response model for user creation.

    This model is used to represent the response returned when a user is created
    or retrieved from the system. It includes the user's ID, name, and email address.

    Attributes:
        user_id (int): The unique identifier for the user.
        name (str): The name of the user.
        email (str): The email address of the user.
    """

    user_id: int
    name: str
    email: str

    class Config:
        title = "User Response Model"
        description = "Response model for user creation."
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
            }
        }

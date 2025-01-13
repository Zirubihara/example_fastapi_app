from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    """
    Response model for user data.

    This model represents the response returned when a user is created
    or retrieved from the system.

    Attributes:
        user_id (int): Unique identifier for the user
        name (str): User's first name
        surname (str): User's surname
        email (EmailStr): User's email address
    """

    user_id: int
    name: str
    surname: str
    email: EmailStr

    model_config = ConfigDict(
        title="User Response Model",
        description="Response model for user operations.",
        json_schema_extra={
            "example": {
                "user_id": 1,
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@example.com",
            }
        },
    )

    def full_name(self) -> str:
        """
        Get user's full name.

        Returns:
            str: User's full name (name + surname)
        """
        return f"{self.name} {self.surname}"

    def to_public_dict(self) -> dict:
        """
        Convert user data to a dictionary, excluding sensitive information.

        Returns:
            dict: Public user information
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
        }

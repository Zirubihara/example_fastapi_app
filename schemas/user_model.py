from pydantic import BaseModel, EmailStr, field_validator, model_validator


class User(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr

    @field_validator("email")
    def email_must_be_gmail(cls, v):
        if not v.endswith("@gmail.com"):
            raise ValueError("Email must be a Gmail address (ending with @gmail.com)")
        return v

    @model_validator(mode="after")
    def name_and_surname_must_be_different(cls, values):
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

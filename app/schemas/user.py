from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    name: Optional[str] = None
    surname: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str
    name: str
    surname: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool = False

    class Config:
        from_attributes = True 
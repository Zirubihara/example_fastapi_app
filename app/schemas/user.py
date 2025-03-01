from typing import Optional
from pydantic import BaseModel, EmailStr, constr

from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    name: constr(min_length=2, max_length=50)
    surname: constr(min_length=2, max_length=50)

class UserCreate(UserBase):
    password: constr(min_length=8)
    role: Optional[UserRole] = UserRole.USER

class UserUpdate(UserBase):
    password: Optional[constr(min_length=8)] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True 
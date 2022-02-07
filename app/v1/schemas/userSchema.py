from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = "yourpassword"


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    user_type: int


class UserCreationSchema(UserBase):
    password: str


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    user_type: Optional[int]
    is_active: Optional[bool]
    updated_at: Optional[datetime]


class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True

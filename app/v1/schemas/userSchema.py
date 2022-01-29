from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserUpdateSchema(BaseModel):
    username: Optional[str]


class UserInDB(UserBase):
    usr_id: int

    class Config:
        orm_mode = True

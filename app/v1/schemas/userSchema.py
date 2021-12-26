from pydantic import BaseModel

class UserBase(BaseModel):
  username: str

class UserInDB(UserBase):
  usr_id: int

  class Config:
    orm_mode = True
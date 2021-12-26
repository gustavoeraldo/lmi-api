from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for Users
class UserBase(BaseModel):
  username: str

class UserInDB(UserBase):
  usr_id: int

  class Config:
    orm_mode = True


# Schema for Measurements
class MeasurementsBase(BaseModel):
  user_id: int
  measure: float
  type_id: int
  tag: Optional[str]

  class Config:
    schema_extra = {
      "example":{
        "user_id": 5,
        "measure": 75.6,
        "type_id": 1,
        "tag": "Sensor 1"
      }
    }

class MeasurementsInDB(MeasurementsBase):
  measure_id: int
  created_at: datetime
  deleted_at: Optional[datetime]

  class Config:
    orm_mode = True


#  Schemas for Measurements types
class MeasurementsTypeBase(BaseModel):
  description: str

  class Config:
    schema_extra = {
      "example": {
        "description": "Tensão"
      }
    }

class MeasureTypesDB(MeasurementsTypeBase):
  id: int

  class Config:
    orm_mode = True


class Pagination(BaseModel):
  page: int = 0
  limit: int = 100
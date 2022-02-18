from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MeasureType(BaseModel):
    m_type_id: int
    description: str

    class Config:
        orm_mode = True


class MeasurementUpdateSchema(BaseModel):
    type_id: Optional[int]
    user_id: Optional[int]
    measure: Optional[float]
    tag: Optional[str]


class MeasurementsBase(BaseModel):
    user_id: int
    measure: float
    type_id: int
    tag: Optional[str]

    class Config:
        schema_extra = {
            "example": {"user_id": 5, "measure": 75.6, "type_id": 1, "tag": "Sensor 1"}
        }


class MeasurementsInDB(MeasurementsBase):
    measure_id: int
    created_at: datetime
    deleted_at: Optional[datetime]

    value_types: MeasureType

    class Config:
        orm_mode = True


class MeasurementsFilters(BaseModel):
    page: Optional[int]
    limit: Optional[int]
    measurement_type: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]


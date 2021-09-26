from pydantic import BaseModel, Field
from typing import Optional

class MeasurementsFilters(BaseModel):
    page: Optional[int]
    limit: Optional[int]
    measurement_type: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]

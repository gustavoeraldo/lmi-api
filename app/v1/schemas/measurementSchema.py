from pydantic import BaseModel, Field
from typing import Optional

class MeasurementsFilters(BaseModel):
    page: Optional[int]
    limit: Optional[int]
    measure_type: Optional[str]
from typing import Any, Dict, Union
from sqlalchemy.orm import Session

from app.v1.controllers import CRUDBase
from app.v1.schemas import MeasurementUpdateSchema, MeasurementsBase
from app.v1.models import Measurements


class MeasurementsCRUD(
    CRUDBase[Measurements, MeasurementsBase, MeasurementUpdateSchema]
):
    def update(
        self,
        db: Session,
        *,
        db_obj: Measurements,
        obj_in: Union[MeasurementUpdateSchema, Dict[str, Any]]
    ) -> Measurements:
        my_measurement = db.query(self.model).filter(self.model.measure_id == 8).first()
        return super().update(db, db_obj=my_measurement, obj_in=obj_in)


measurements = MeasurementsCRUD(Measurements)

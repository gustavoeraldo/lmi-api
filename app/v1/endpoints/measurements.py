from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.v1.schemas.globalSchema import MeasurementsBase, MeasurementsInDB
from app.v1.database.mainDB import get_db
from app.v1.controllers.measuresController import MeasuresController

router = APIRouter()

@router.get('/{usr_id}')
async def read_measurements(
  usr_id: int, 
  measurement_type: Optional[int] = Query(1, gt=0),
  page: Optional[int] = Query(1, pattern=r'^[0-9]', gt=0),
  limit: Optional[int] = Query(100, pattern=r'^[0-9]', gt=0),
  db: Session = Depends(get_db)):
  """
  Return all measurements.
  """

  measurements = MeasuresController.get_measurements(
    db, usr_id, measurement_type)
  return measurements


@router.post('', response_model=MeasurementsInDB)
async def add_measurement(*,
  measure_in: MeasurementsBase, 
  db: Session = Depends(get_db)):
  """
  Add new measurements
  """
  new_measurement = MeasuresController.create_measurements(db, measure_in)

  return new_measurement

@router.delete('/{measurement_id}')
async def remove_measurement(user_id: int, measurement_id: int, db: Session = Depends(get_db)):
  MeasuresController.delete_measurements(db=db, measurement_id=measurement_id, user_id=user_id)
  return JSONResponse(status_code=status.HTTP_200_OK, content='Measurement was deleted.')
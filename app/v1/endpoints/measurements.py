from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.v1.schemas.globalSchema import MeasurementsBase, MeasurementsInDB
from app.v1.database.mainDB import get_db
from app.v1.controllers.measuresController import MeasuresController
from app.v1.schemas.measurementSchema import MeasurementsFilters
from app.v1.schemas.globalSchema import Pagination

router = APIRouter()

@router.get('')
async def get_all_measurements(*,
  user_id: Optional[int],
  measurement_type: Optional[int] = Query(1),
  tag: Optional[str] = Query('sensor 1'),
  page: Optional[int] = Query(0, pattern=r'^[0-9]'),
  limit: Optional[int] = Query(100, pattern=r'^[0-9]', gt=0),
  db: Session = Depends(get_db)):

  filters = {
    'user_id': user_id,
    'type_id': measurement_type,
    'tag': tag.lower(),
  }

  pagination = Pagination(
    page = page,
    limit = limit,
  )

  measures = await MeasuresController.\
    get_test_measures(db, filters, pagination)
  return measures

@router.get('/{usr_id}')
async def read_measurements(
  usr_id: int, 
  measurement_type: Optional[str] = Query('temperature'),
  page: Optional[int] = Query(1, pattern=r'^[0-9]', gt=0),
  limit: Optional[int] = Query(100, pattern=r'^[0-9]', gt=0),
  start_date: Optional[str] = Query(datetime.now().strftime("%Y-%m-%d")),
  end_date: Optional[str] = Query(datetime.now().strftime("%Y-%m-%d")),
  db: Session = Depends(get_db)):
  """
  Return all measurements.
  """

  filters = MeasurementsFilters(
    page = page,
    limit = limit,
    measurement_type = measurement_type.lower(),
    start_date = start_date,
    end_date = end_date
  )

  measurements = MeasuresController.get_measurements(db, usr_id, filters)
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
from sqlalchemy.sql.expression import extract
from fastapi import status
from datetime import date
from sqlalchemy.orm import Session, load_only

from app.v1.models.measurementsModel import Measurements
from app.v1.models.measureTypesModel import MeasuresType
from app.v1.schemas.globalSchema import MeasurementsBase, MeasurementsInDB
from app.v1.exceptions.globalException import GlobalException
from app.v1.schemas.measurementSchema import MeasurementsFilters

class MeasurementsController(Measurements):
  def __init__(self, model) -> None:
    self.model = model
  
  def create_measurements(self, db: Session, measure_in: MeasurementsBase) -> MeasurementsInDB:
    db_measurement = Measurements(
      user_id = measure_in.user_id,
      type_id = measure_in.type_id,
      measure = measure_in.measure,
      tag = measure_in.tag
    )
    try:
      db.add(db_measurement)
      db.commit()
      db.refresh(db_measurement)
    except Exception as e:
      raise GlobalException(400, f'Something went wrong trying to insert the data!\nError:{e}')

    return db_measurement

  # Get all measurements from an User
  def get_measurements(self, db: Session, user_id: int, filters: MeasurementsFilters):
    if filters.start_date != filters.end_date:
      return self.get_measurements_by_date(db, user_id, filters)
    
    return db.query(Measurements)\
      .join(
        MeasuresType, 
        Measurements.type_id == MeasuresType.m_type_id)\
      .filter(
        Measurements.user_id == user_id,
        MeasuresType.description == filters.measurement_type)\
      .options(load_only('measure', 'tag', 'created_at'))\
      .order_by(Measurements.created_at.asc())\
      .limit(filters.limit).all()

  def get_measurements_by_date(self, db: Session, user_id: int, filters: MeasurementsFilters):
    measurements_list = db.query(Measurements)\
      .join(
        MeasuresType, 
        Measurements.type_id == MeasuresType.m_type_id)\
      .filter(
        Measurements.user_id == user_id,
        MeasuresType.description == filters.measurement_type,
        Measurements.created_at >= filters.start_date,
        Measurements.created_at < filters.end_date)\
      .options(load_only('measure', 'tag', 'created_at'))\
      .order_by(Measurements.created_at.asc())\
      .limit(filters.limit).all()

    return measurements_list

  # Get only 1 measurement
  def get_measurement(self, db: Session, user_id: int, measurement_id: int):
    return db.query(Measurements).filter(
      Measurements.user_id == user_id, 
      Measurements.measure_id == measurement_id).first()


  def delete_measurements(self, db: Session, measurement_id: int, user_id: int):

    if not self.get_measurement(db, user_id, measurement_id):
      raise GlobalException(status_code=status.HTTP_404_NOT_FOUND, message='Measurement not found!')

    db.query(Measurements).filter(
      Measurements.user_id == user_id, 
      Measurements.measure_id == measurement_id).delete()
    db.commit()
    return True

  # Get measurements with filters
  def get_specific_measures(
    self, db: Session, user_id: int, m_tag: str, m_type_id: int, date_time: date
    ) -> MeasurementsInDB:
    return db.query(Measurements)\
      .filter(
        Measurements.user_id == user_id,
        Measurements.type_id == m_type_id,
        Measurements.tag == m_tag,
        Measurements.created_at == date_time
      )\
      .all()

MeasuresController = MeasurementsController(Measurements)

from typing import List
from sqlalchemy.orm import Session

from app.v1.models.measureTypesModel import MeasuresType
from app.v1.schemas.globalSchema import MeasurementsTypeBase, MeasureTypesDB
from app.v1.exceptions.globalException import GlobalException

class MeasureTypesController(MeasuresType):
  def __init__(self, model) -> None:
    self.model = model

  def create_measure_type(self, measure_t: str, db: Session):
    verif_type = self.get_type(measure_t, db)

    if verif_type:
      raise GlobalException(400, 'Measurement Type already exists.')

    db_measure_type = MeasuresType(
      description = measure_t.lower(),
    )
    
    try:
      db.add(db_measure_type)
      db.commit()
      db.refresh(db_measure_type)
    except Exception as e:
      raise GlobalException(400, f'Error trying to insert data in database! {e}')

    return db_measure_type


  def get_measure_types(self, db: Session)->List[MeasureTypesDB]:
    return db.query(MeasuresType).order_by(MeasuresType.description).all()


  def get_type(self, m_type: str, db: Session)->MeasurementsTypeBase:
    return db.query(MeasuresType).filter(MeasuresType.description == m_type).first()


  def delete_measure_type(self, m_type_id: int, db: Session):
    if not self.get_type(m_type_id, db):
      raise GlobalException(404, 'Measurement type not found!')
    
    db.query(MeasuresType).filter(MeasuresType.m_type_id == m_type_id).delete()
    db.commit()
    return True

MeasuresTypesC = MeasureTypesController(MeasuresType)

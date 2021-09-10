from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.v1.schemas.globalSchema import MeasurementsTypeBase
from app.v1.database.mainDB import get_db
from app.v1.controllers.valuesTypeController import MeasuresTypesC

router = APIRouter()

@router.post('/')
async def add_measure_type(
  measure_type: MeasurementsTypeBase, db: Session = Depends(get_db)):
  """
    Add a new measurement type
  """
  new_measure_type = MeasuresTypesC.create_measure_type(measure_type.description.lower(), db)
  return new_measure_type


@router.get('/')
async def read_measure_types(db: Session = Depends(get_db)):
  measure_type = MeasuresTypesC.get_measure_types(db)

  return measure_type


@router.delete('/{m_type_id}')
async def remove_measure_type(m_type_id: int, db: Session = Depends(get_db)):
  deleted_m_type = MeasuresTypesC.delete_measure_type(m_type_id=m_type_id, db=db)
  return deleted_m_type
from sqlalchemy import Column, ForeignKey, Integer, DateTime, Float, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.v1.database.mainDB import Base

class Measurements(Base):
  __tablename__ = 'measurements'

  measure_id = Column(Integer, primary_key=True, index=True)
  type_id = Column(Integer, ForeignKey('value_types.m_type_id'), nullable=False)
  user_id = Column(Integer, ForeignKey('users.usr_id'), index=True, nullable=False)
  measure = Column(Float, index=True, nullable=False)
  tag = Column(String(20), index=True)
  created_at = Column(DateTime(timezone=True), index=True, default=func.now())
  deleted_at = Column(DateTime, index=True)

  # relationships
  measure_type = relationship("MeasuresType")
  user = relationship("Users")

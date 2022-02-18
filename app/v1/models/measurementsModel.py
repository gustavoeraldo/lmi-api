from sqlalchemy import Column, ForeignKey, Integer, DateTime, Float, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.v1.database.mainDB import Base


class Measurements(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("value_types.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    measure = Column(Float, nullable=False)
    tag = Column(String(20))
    created_at = Column(DateTime(timezone=True), default=func.now())
    deleted_at = Column(DateTime)

    # relationships
    measure_type = relationship("MeasuresType")
    user = relationship("Users")

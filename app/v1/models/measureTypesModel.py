from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

from app.v1.database.mainDB import Base


class MeasuresType(Base):
    __tablename__ = "value_types"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100), index=True, nullable=False)

    # Relationships
    measurements = relationship(
        "Measurements", backref=backref("value_types", lazy="joined")
    )

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.v1.database.mainDB import Base

class Users(Base):
  __tablename__ = 'users'

  usr_id = Column(Integer, primary_key=True, index=True)
  username = Column(String(60), index=True, nullable=False)

  measurements = relationship('Measurements')

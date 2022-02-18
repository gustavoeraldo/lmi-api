from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.v1.database.mainDB import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(60), index=True, nullable=False)
    first_name = Column(String(60), index=True, nullable=False)
    last_name = Column(String(60), nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Integer, ForeignKey("user_type.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    deleted_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)

    user_type_relation = relationship("UserType")

class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True)
    name = Column(String)

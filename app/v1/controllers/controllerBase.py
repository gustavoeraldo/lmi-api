from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.v1.database.base_class import Base
from app.v1.schemas import Pagination

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Base)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Base)
FilterSchemaType = TypeVar("FilterSchemaType", bound=Base)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, FilterSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_resource_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multiple(
        self, db: Session, *, limit: int = 100, offset: int = 0
    ) -> List[ModelType]:
        return db.query(self.model).limit(limit).offset(offset).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(self, db: Session, *, id: Any) -> ModelType:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        db.delete(db_obj)
        db.commit()

        return db_obj

    def get_by_single_attr(self, db: Session, filter_data: dict) -> ModelType:
        [(attr, value)] = filter_data.items()
        return db.query(self.model).filter(getattr(self.model, attr) == value).first()

    def get_by_multiple_filters(
        self,
        db: Session,
        filters: Union[FilterSchemaType, Dict[str, Any]],
        pagination: Pagination,
    ) -> List[ModelType]:
        query = db.query(self.model)

        filters_in = filters.dict(exclude_unset=True, exclude_none=True)

        for attr, value in filters_in.items():
            if isinstance(value, str):
                query = query.filter(
                    func.lower(getattr(self.model, attr)).like(f"%{value.lower()}%")
                )
            if isinstance(value, int):
                query = query.filter(getattr(self.model, attr) == value)
            if isinstance(value, list):
                query = query.filter(getattr(self.model, attr).in_(value))

        query = query.limit(pagination.limit).offset(pagination.page)

        return query.all()

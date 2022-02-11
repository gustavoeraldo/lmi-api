from typing import Any, Dict, Optional, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from typing import List, Dict, Any

from app.v1.controllers.controllerBase import CRUDBase
from app.v1.schemas import (
    UserCreationSchema,
    UserUpdateSchema,
    UserBase,
    UserFilters,
    Pagination,
)
from app.v1.models.usersModel import Users
from app.v1.controllers.authController import Auth
from app.v1.schemas import TokenPayload
from app.v1.core import settings
from app.v1.database import get_db

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


class UserCRUD(CRUDBase[Users, UserCreationSchema, UserUpdateSchema, UserFilters]):
    def get_by_any_attr(self, db: Session, data: Dict[str, Any]) -> Optional[Users]:
        return super().get_by_single_attr(db, filter_data=data)

    def get_by_multiple_attributes(
        self,
        db: Session,
        filters: Union[UserFilters, Dict[str, Any]],
        pagination: Pagination,
    ) -> Optional[List[Users]]:
        return super().get_by_multiple_filters(db, filters, pagination)

    def get_by_id(self, db: Session, id: Any) -> Users:
        return super().get_resource_by_id(db, id)

    def get_by_email(self, db: Session, email: str) -> Optional[Users]:
        return db.query(self.model).filter(self.model.email == email).first()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[Users]:
        current_user = self.get_by_email(db, email)

        if not current_user:
            raise HTTPException(
                status_code=404, detail="Email not found or wrong email"
            )

        if not Auth.verify_password(password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Wrong password, try again.")

        return current_user

    def get_multiple(self, db: Session) -> List[UserBase]:
        return super().get_multiple(db=db, limit=10, offset=0)

    def create(self, db: Session, *, user_data: UserCreationSchema) -> Optional[Users]:
        new_user = jsonable_encoder(user_data)
        new_user["hashed_password"] = Auth.get_hashed_password(user_data.password)

        del new_user["password"]
        user_db = Users(**new_user)

        return super().create(db=db, obj_in=user_db)

    def update(
        self,
        db: Session,
        *,
        db_obj: Users,
        obj_in: Union[UserUpdateSchema, Dict[str, Any]]
    ) -> Users:

        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self):
        return

    def get_current_user(
        self, db: Session = Depends(get_db), token: str = Depends(oauth2)
    ) -> Users:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            token_data = TokenPayload(**payload)
        except (JWTError, ValidationError):
            raise HTTPException(status_code=404, detail="User not found.")

        user_db = self.get_by_id(db, id=token_data.id)

        print(user_db.is_active)
        if not user_db.is_active:
            raise HTTPException(
                status_code=423,
                detail="User is not active. Request an activation for a ADMIN user.",
            )

        if not user_db:
            raise HTTPException(status_code=404, detail="User not found.")

        return user_db


user = UserCRUD(Users)

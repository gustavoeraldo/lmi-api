from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from app.v1.controllers import CRUDBase
from app.v1.schemas import UserBase, UserUpdateSchema
from app.v1.models.usersModel import Users

# from app.v1.exceptions.globalException import GlobalException


class UserCRUD(CRUDBase[Users, UserBase, UserUpdateSchema]):
    def update(
        self,
        db: Session,
        *,
        db_obj: Users,
        obj_in: Union[UserUpdateSchema, Dict[str, Any]]
    ) -> Users:
        my_user = db.query(self.model).filter(self.model.usr_id == 8).first()
        return super().update(db, db_obj=my_user, obj_in=obj_in)

user = UserCRUD(Users)
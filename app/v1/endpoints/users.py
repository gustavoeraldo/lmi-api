from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.v1.schemas import UserUpdateSchema, UserCreationSchema, UserInDB, UserBase
from app.v1.database.mainDB import get_db
from app.v1.models.usersModel import Users

from app.v1.controllers.testUser import user

router = APIRouter()


@router.get(
    "",
    response_model=List[UserBase],
    description="""
    Return all users
    """,
)
async def get_all_users(
    db: Session = Depends(get_db), current_user: Users = Depends(user.get_current_user)
):
    return user.get_multiple(db=db)


@router.get(
    "/one/{first_name}",
    # response_model=List[UserBase],
    description="""
    Return one user
    """,
)
async def get_all_users(
    db: Session = Depends(get_db), first_name: Optional[str] = None
):
    filter_data = {"first_name": first_name}
    return user.get_by_any_attr(db, filter_data)


@router.post("", response_model=UserBase, description="")
async def create_user(
    *,
    user_in: UserCreationSchema,
    db: Session = Depends(get_db),
    current_user: Users = Depends(user.get_current_user)
):
    return user.create(db=db, user_data=user_in)


# @router.delete("/{user_id}")
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     deleted_user = UsersControllers.delete_user(db=db, user_id=user_id)

#     return {
#         "message": f"User {deleted_user.username} was deleted!Id = {deleted_user.usr_id}"
#     }


@router.patch("/{user_id}")
async def update_user(
    *, db: Session = Depends(get_db), user_id: int, user_in: UserUpdateSchema
):
    # updated_usr = UsersControllers.update_user(
    #     db=db, user_id=user_id, user_new_name=user_in
    # )
    old_user = UserInDB(usr_id=8, username="Thales")
    return user.update(db, db_obj=old_user, obj_in=user_in)

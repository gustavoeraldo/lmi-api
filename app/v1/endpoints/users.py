from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import EmailStr

from app.v1.database.mainDB import get_db
from app.v1.models.usersModel import Users
from app.v1.controllers.testUser import user
from app.v1.schemas import (
    UserUpdateSchema,
    UserCreationSchema,
    UserBase,
    Pagination,
    UserFilters,
    UserDefaultResponse,
)

router = APIRouter()

@router.get(
    "",
    response_model=Optional[List[UserDefaultResponse]],
    description=("""
    Return multiple users. You can apply several filters to 
    retrive users information.
    """),
)
async def get_all_users(
    *,
    db: Session = Depends(get_db),
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[EmailStr] = None,
    is_active: Optional[bool] = True,
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    current_user: Users = Depends(user.get_current_user)
):
    if current_user.user_type != 1:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to retrive this information.",
        )

    filters = UserFilters(
        first_name = first_name,
        last_name = last_name,
        email = email,
        is_active = is_active,
    )

    pagination = Pagination(page=offset, limit=limit)
    # users = user.get_by_multiple_attributes(db, filters, pagination)
    
    return user.get_by_multiple_attributes(db, filters, pagination)

@router.post("", response_model=UserBase, description="")
async def create_user(
    *,
    user_in: UserCreationSchema,
    db: Session = Depends(get_db),
    current_user: Users = Depends(user.get_current_user)
):
    if current_user.user_type != 1:
        raise HTTPException(
            status_code=403, detail="You do not have permisstion to create users."
        )

    return user.create(db=db, user_data=user_in)


# @router.delete("/{user_id}")
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     deleted_user = UsersControllers.delete_user(db=db, user_id=user_id)

#     return {
#         "message": f"User {deleted_user.username} was deleted!Id = {deleted_user.usr_id}"
#     }


@router.patch("/{user_id}", response_model=UserBase, description="")
async def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdateSchema,
    current_user: Users = Depends(user.get_current_user)
):
    if current_user.user_type != 1 and current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="You do not have permisstion to edit this user."
        )

    old_user = user.get_by_id(db, id=user_id)

    return user.update(db, db_obj=old_user, obj_in=user_in)


# @router.patch("/{user_id}")
# async def update_user_type():
#     return

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.v1.controllers.usersController import UsersControllers
from app.v1.schemas.globalSchema import UserBase, UserInDB
from app.v1.database.mainDB import get_db

router = APIRouter()

@router.get('', response_model=List[UserInDB])
async def get_all_users(db: Session = Depends(get_db)):
  """
  Return all users
  """
  listOfUsers = UsersControllers.get_all_users(db=db)
  return listOfUsers


@router.post('', response_model=UserInDB)
async def create_user(user_in: UserBase, db: Session = Depends(get_db)):
  new_usr = UsersControllers.create_user(db=db, user_in=user_in)
  return new_usr


@router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
  deleted_user = UsersControllers.delete_user(db=db, user_id=user_id)
  
  return {
    "message": f'User {deleted_user.username} was deleted!Id = {deleted_user.usr_id}'
  }

@router.patch('/{user_id}')
async def update_user(user_id: int, user_in: UserBase, db: Session = Depends(get_db)):
  updated_usr = UsersControllers.update_user(db=db, user_id=user_id, user_new_name=user_in)
  return updated_usr
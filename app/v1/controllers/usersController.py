from typing import List
from sqlalchemy.orm import Session

from app.v1.schemas.globalSchema import UserBase, UserInDB
from app.v1.models.usersModel import Users
from app.v1.exceptions.globalException import GlobalException

class UsersController(Users):
  def __init__(self, model) -> None:
    self.model = model

  def create_user(self, db: Session, user_in: UserBase) -> UserInDB:
    db_user = Users(
      username = user_in.username,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


  def get_all_users(self, db: Session) -> List[UserInDB]:
    return db.query(Users).order_by(Users.username).all()

  
  def get_user(self, db: Session, user_id: int ) -> UserInDB:
    return db.query(Users).filter(Users.usr_id == user_id).first()


  def delete_user(self, db: Session, user_id: int) -> UserInDB:
    verify_user = self.get_user(db, user_id)

    if not verify_user:
      raise GlobalException(404, 'User not found!')
    
    # db.delete(Users).filter(Users.usr_id == user_id).first()
    db.query(Users).filter(Users.usr_id == user_id).delete()
    db.commit()
    return verify_user


  def update_user(self, db: Session, user_id: int, user_new_name: UserBase) -> UserBase:
    verify_user = self.get_user(db, user_id)

    if not verify_user:
      raise GlobalException(404, 'User not found')

    updated_user = db.query(Users).filter(Users.usr_id == user_id)\
      .update(dict(username = user_new_name.username))
    db.commit()
    return updated_user

UsersControllers = UsersController(Users)

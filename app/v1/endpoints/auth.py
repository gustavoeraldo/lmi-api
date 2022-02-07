from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.v1.database import get_db
from app.v1.controllers.testUser import user
from app.v1.controllers.authController import Auth
from app.v1.schemas import TokenSchema, UserLoginSchema

router = APIRouter()


@router.post("/token", response_model=TokenSchema)
async def get_token(credentials: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = user.authenticate(db, credentials.email, credentials.password)

    access_token = Auth.create_access_token(data={"id": user_db.id})

    return TokenSchema(access_token=access_token)


@router.post("/login", response_model=TokenSchema, include_in_schema=False)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_db = user.authenticate(db, form_data.username, form_data.password)

    access_token = Auth.create_access_token(data={"id": user_db.id})

    return TokenSchema(access_token=access_token)

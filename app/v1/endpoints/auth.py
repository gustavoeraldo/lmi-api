from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from datetime import timedelta

from app.v1.database import get_db
from app.v1.controllers.testUser import user
from app.v1.controllers.authController import Auth
from app.v1.schemas import TokenSchema, UserLoginSchema
from app.v1.core import settings


router = APIRouter()


class Settings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY
    access_expires: int = timedelta(minutes=10)
    refresh_expires: int = timedelta(days=10)
    authjwt_decode_algorithms: set = {"HS256"}


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/token", response_model=TokenSchema)
async def get_token(credentials: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = user.authenticate(db, credentials.email, credentials.password)

    access_token = Auth.create_access_token(data={"id": user_db.id})

    return TokenSchema(access_token=access_token)


@router.post("/login", response_model=TokenSchema, include_in_schema=False)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user_db = user.authenticate(db, form_data.username, form_data.password)

    access_token = Auth.create_access_token(data={"id": user_db.id})

    return TokenSchema(access_token=access_token)

# Testando refresh tokens
@router.post("/token-test", include_in_schema=False)
async def get_token(
    credentials: UserLoginSchema,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    user_db = user.authenticate(db, credentials.email, credentials.password)

    access_token = Authorize.create_access_token(subject=user_db.id)
    refresh_token = Authorize.create_refresh_token(subject=user_db.id)

    return {"access_token": access_token, "refresh_token": refresh_token}

# Testando refresh tokens
@router.post("/refresh", include_in_schema=False)
async def refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    return {"access_token": new_access_token}

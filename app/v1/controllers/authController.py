from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.v1.core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationController:
    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Creates an access token, type Bearer."""

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, "HS256")

        return encoded_jwt

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    def get_hashed_password(self, password: str):
        return pwd_context.hash(password)




Auth = AuthenticationController()

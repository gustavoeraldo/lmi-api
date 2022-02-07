from typing import Any, Dict, List, Optional
from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, PostgresDsn, validator
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

SQLACHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
_SECRET_KEY = os.getenv("SECRET_KEY")
ORIGINS = os.getenv("ORIGINS")


class Settings(BaseSettings):
    API_PATH_VERSION: str = "/lmi/v2"
    SECRET_KEY: str = _SECRET_KEY
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SERVER_NAME: str = "LMI"
    SERVER_HOST: Optional[AnyHttpUrl]

    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ORIGINS

    PROJECT_NAME: str = "LMI API"
    SENTRY_DNS: Optional[HttpUrl] = None

    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = SQLACHEMY_DATABASE_URL

    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str:Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         schema="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB')}",
    #     )

    # class Config:
    #     case_sensitive = True


settings = Settings()

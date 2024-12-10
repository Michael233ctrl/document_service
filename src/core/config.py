import os

from dotenv import load_dotenv, find_dotenv
from pydantic import EmailStr

from pydantic_settings import BaseSettings

load_dotenv(dotenv_path=find_dotenv())


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("DOCS_PROJECT_NAME")
    SERVER_NAME: str = os.getenv("DOCS_SERVER_NAME")
    API_V1_STR: str = os.getenv("DOCS_API_V1_STR")

    # JWT config
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    TOTP_SECRET_KEY: str = os.getenv("TOTP_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_SECONDS: int = os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS")
    REFRESH_TOKEN_EXPIRE_SECONDS: int = os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS")
    JWT_ALGO: str = os.getenv("JWT_ALGORITHM")

    AUTH_URL: str = os.getenv('AUTH_URL')

    # Mongo config
    MONGO_DATABASE_URI: str = os.getenv("MONGO_DATABASE_URI")
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE")
    if os.getenv("MONGO_REPLICA_SET"):
        MONGO_DATABASE = MONGO_DATABASE+f'&replicaSet={os.getenv("MONGO_REPLICA_SET_NAME")}'

    FIRST_SUPERUSER: EmailStr = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")


settings = Settings()

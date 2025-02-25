import os

from dotenv import find_dotenv, load_dotenv
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

    # Auth server
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL")
    AUTH_API_V1_STR: str = os.getenv("AUTH_API_V1_STR")
    OAUTH_URL: str = os.getenv("OAUTH_URL")
    AUTH_URL: str = AUTH_SERVICE_URL + AUTH_API_V1_STR + OAUTH_URL
    GET_USER_URL: str = AUTH_SERVICE_URL + API_V1_STR + "/users/me"

    # Mongo config
    MONGO_DATABASE_URI: str = os.getenv("MONGO_DATABASE_URI")
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE")
    if os.getenv("MONGO_REPLICA_SET"):
        MONGO_DATABASE = (
            MONGO_DATABASE + f'&replicaSet={os.getenv("MONGO_REPLICA_SET_NAME")}'
        )

    FIRST_SUPERUSER: EmailStr = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")

    LIMIT_OF_DOCUMENT_VERSIONS: int = 5


settings = Settings()

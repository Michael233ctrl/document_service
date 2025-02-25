import httpx
from typing import Generator

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from motor.core import AgnosticDatabase

from src import models
from src.core.config import settings
from src.db.session import MongoDatabase


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=settings.AUTH_URL)


def get_db() -> Generator:
    try:
        db = MongoDatabase()
        yield db
    finally:
        pass


async def get_current_user(
    db: AgnosticDatabase = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.GET_USER_URL,
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Authentication failed"
        )
    user_data = response.json()
    return models.User(**user_data)

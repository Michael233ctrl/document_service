from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.api.api import api_router
from src.core.config import settings


@asynccontextmanager
async def app_init(app: FastAPI):
    app.include_router(api_router, prefix=settings.API_V1_STR)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=app_init,
)

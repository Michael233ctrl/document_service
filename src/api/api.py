from fastapi import APIRouter, status

from src.api.v1.endpoints import documents
from src.schemas.healthcheck import HealthCheck

api_router = APIRouter()


@api_router.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")


api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
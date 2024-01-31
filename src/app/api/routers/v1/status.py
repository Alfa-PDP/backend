import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.services import create_status_service
from app.schemas.api_status import APIStatusSchema
from app.services.status import StatusService

router = APIRouter(prefix="/status", tags=["Status"])

logger = logging.getLogger().getChild("status-router")

StatusServiceDep = Annotated[StatusService, Depends(create_status_service)]


@router.get(
    "",
    summary="Получить статус API",
    response_model=APIStatusSchema,
    status_code=status.HTTP_200_OK,
)
async def _get_api_status(status_service: StatusServiceDep) -> APIStatusSchema:
    logger.debug("Get api status")
    return await status_service.get_api_status()

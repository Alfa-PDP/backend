import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.deps.services import create_status_service
from app.schemas.status import StatusSchema
from app.services.status import StatusServiceABC

router = APIRouter(prefix="/status", tags=["Status"])

logger = logging.getLogger().getChild("status-router")

StatusService = Annotated[StatusServiceABC, Depends(create_status_service)]


@router.get(
    "",
    summary="Получить статус API",
    response_model=StatusSchema,
    status_code=status.HTTP_200_OK,
)
async def _get_api_status(status_service: StatusService) -> StatusSchema:
    logger.debug("Get api status")
    return await status_service.get_api_status()

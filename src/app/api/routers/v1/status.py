import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.services import create_api_status_service
from app.schemas.api_status import APIStatusSchema
from app.services.api_status import APIStatusService

router = APIRouter(prefix="/status", tags=["Status"])

logger = logging.getLogger().getChild("status-router")

StatusServiceDep = Annotated[APIStatusService, Depends(create_api_status_service)]


@router.get(
    "",
    summary="Получить статус API",
    response_model=APIStatusSchema,
    status_code=status.HTTP_200_OK,
)
async def _get_api_status(status_service: StatusServiceDep) -> APIStatusSchema:
    """
    Получение статуса API.

    Args:
        - status_service (StatusServiceDep): Сервис для работы со статусом API.

    Returns:
        - APIStatusSchema: Информация о статусе API.
    """
    logger.debug("Get api status")
    return await status_service.get_api_status()

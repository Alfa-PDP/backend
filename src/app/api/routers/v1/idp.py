import logging
from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies.services import IDPServiceDep
from app.api.request_model.idp import IDPQueryParamsDep
from app.schemas.idp import IDPCreateSchema, IDPFilter, IDPGetExtendedSchema, IDPProgressSchema

router = APIRouter(prefix="/idp", tags=["IDP"])

logger = logging.getLogger().getChild("idp-router")


@router.post(
    "",
    summary="Добавить ИПР",
    status_code=status.HTTP_201_CREATED,
)
async def create_idp(idp_service: IDPServiceDep, idp_data: IDPCreateSchema) -> None:
    """
    Создание ИПР для сотрудника.

    Args:
        - idp_service (IDPServiceDep): Сервис для работы с ИПР.
        - idp_data (IDPCreateSchema): Данные для создания ИПР.
    """
    logger.debug(f"Create IDP with {idp_data}")
    await idp_service.create(idp_data)


@router.get(
    "/{user_id}",
    summary="Открыть карточку ИПР сотрудника",
    response_model=IDPGetExtendedSchema,
    status_code=status.HTTP_200_OK,
)
async def get_idp(user_id: UUID, idp_service: IDPServiceDep, query_params: IDPQueryParamsDep) -> IDPGetExtendedSchema:
    """
    Получение информации по ИПР для сотрудника.

    Args:
        - user_id (UUID): Идентификатор сотрудника.
        - idp_service (IDPServiceDep): Сервис для работы с ИПР.
        - query_params (IDPQueryParamsDep): Параметры запроса.

    Returns:
        - IDPGetExtendedSchema: Расширенная информация по ИПР.
    """
    logger.debug(f"Get IDP for user {user_id}")
    filters = IDPFilter(year=query_params.year)
    return await idp_service.get_by_user_id(user_id, filters)


@router.get(
    "/{idp_id}/progress",
    summary="Показать прогресс по ИПР сотрудника",
    response_model=IDPProgressSchema,
    status_code=status.HTTP_200_OK,
)
async def get_idp_progress(idp_id: UUID, idp_service: IDPServiceDep) -> IDPProgressSchema:
    """
    Получение информации о прогрессе по ИПР для сотрудника.

    Args:
        - idp_id (UUID): Идентификатор ИПР.
        - idp_service (IDPServiceDep): Сервис для работы с ИПР.

    Returns:
        - IDPProgressSchema: Информация о прогрессе по ИПР.
    """
    logger.debug(f"Get IDP progress for idp id {idp_id}")
    return await idp_service.get_progress(idp_id)

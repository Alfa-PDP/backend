import logging
from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies.services import IDPServiceDep
from app.api.request_model.idp import IDPQueryParamsDep
from app.schemas.idp import IDPCreateSchema, IDPFilter, IDPGetExtendedSchema

router = APIRouter(prefix="/idp", tags=["IDP"])

logger = logging.getLogger().getChild("idp-router")


@router.post(
    "",
    summary="Добавить ИПР",
    status_code=status.HTTP_201_CREATED,
)
async def create_idp(idp_service: IDPServiceDep,
                     idp_data: IDPCreateSchema) -> None:
    logger.debug(f"Create IDP with {idp_data}")
    await idp_service.create(idp_data)


@router.get(
    "/{user_id}",
    summary="Открыть карточку ИПР сотрудника",
    response_model=IDPGetExtendedSchema,
    status_code=status.HTTP_200_OK,
)
async def get_idp(user_id: UUID, idp_service: IDPServiceDep,
                  query_params: IDPQueryParamsDep) -> IDPGetExtendedSchema:
    logger.debug(f"Get IDP for user {user_id}")
    filters = IDPFilter(year=query_params.year)
    return await idp_service.get_by_user_id(user_id, filters)

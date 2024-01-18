import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.services import create_users_service
from app.schemas.users import UserSchema
from app.services.users import UsersService

router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger().getChild("user-router")

UsersServiceDep = Annotated[UsersService, Depends(create_users_service)]


@router.get(
    "",
    summary="Получить всех пользователей",
    response_model=list[UserSchema],
    status_code=status.HTTP_200_OK,
)
async def _get_all_users(users_service: UsersServiceDep) -> list[UserSchema]:
    logger.debug("Get api status")
    return await users_service.get_all_users()

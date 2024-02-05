import logging

from fastapi import APIRouter, status

from app.api.dependencies.repositories import IDPRepositoryDep

router = APIRouter(prefix="/years", tags=["Years"])

logger = logging.getLogger().getChild("years-router")


@router.get(
    "",
    summary="Список годов по ИПР",
    response_model=list[int],
    status_code=status.HTTP_200_OK,
)
async def get_years(idp_repositorty: IDPRepositoryDep) -> list[int]:
    """
    Получение списка годов по ИПР.

    Args:
        - idp_repository (IDPRepositoryDep): Репозиторий для работы с ИПР.

    Returns:
        - List[int]: Список годов.
    """
    logger.debug("Get years")
    return await idp_repositorty.distinct_years()

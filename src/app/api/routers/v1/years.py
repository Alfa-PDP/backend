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
    logger.debug("Get years")
    return await idp_repositorty.distinct_years()

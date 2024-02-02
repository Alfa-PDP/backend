import logging
from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies.repositories import TeamRepositoryDep
from app.schemas.team import TeamSchema

router = APIRouter(prefix="/teams", tags=["Teams"])

logger = logging.getLogger().getChild("teams-router")


@router.get(
    "",
    summary="Список команд",
    response_model=list[TeamSchema],
    status_code=status.HTTP_200_OK,
)
async def get_teams(team_repository: TeamRepositoryDep) -> list[TeamSchema]:
    logger.debug("Get all teams")
    return await team_repository.get_all()


@router.get(
    "/{team_id}",
    summary="Информация о команде",
    response_model=TeamSchema,
    status_code=status.HTTP_200_OK,
)
async def get_team(team_id: UUID,
                   team_repository: TeamRepositoryDep) -> TeamSchema:
    logger.debug(f"Get team with id {team_id}")
    return await team_repository.get_by_id(team_id)

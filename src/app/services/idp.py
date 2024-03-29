from dataclasses import dataclass
from uuid import UUID

from app.domain.user_progress import UserProgress
from app.repositories.idp import AbstractIDPRepository
from app.repositories.tasks import AbstractTaskRepository
from app.repositories.users import AbstractUserRepository
from app.schemas.idp import IDPCreateSchema, IDPFilter, IDPGetExtendedSchema, IDPProgressSchema


@dataclass
class IDPService:
    _idp_repository: AbstractIDPRepository
    _user_repository: AbstractUserRepository
    _tasks_repository: AbstractTaskRepository

    async def create(self, idp_data: IDPCreateSchema) -> None:
        await self._user_repository.get_by_id(idp_data.user_id)
        await self._idp_repository.create(idp_data)

    async def get_by_user_id(self, user_id: UUID, filter: IDPFilter) -> IDPGetExtendedSchema:
        user = await self._user_repository.get_by_id(user_id)
        idp = await self._idp_repository.get_by_user_and_filter(user_id, filter)
        tasks = await self._tasks_repository.get_all_by_idp_id_with_status(idp.id)
        return IDPGetExtendedSchema(
            id=idp.id,
            start_date=idp.start_date,
            end_date=idp.end_date,
            year=idp.year,
            # TODO: Добавить логику подсчёта количества тасок за текущий ИПР. Сейчас счиает общее кол-во.
            user_id=user.id,
            name=user.name,
            family_name=user.family_name,
            middle_name=user.middle_name,
            position=user.position,
            avatar=user.avatar,
            email=user.email,
            phone_number=user.phone_number,
            telegram=user.telegram,
            team_id=user.team_id,
            task_count=len(tasks),
            task_progress=UserProgress(tasks).progress,
            tasks=tasks,
        )

    async def get_progress(self, idp_id: UUID) -> IDPProgressSchema:
        tasks = await self._tasks_repository.get_all_by_idp_id_with_status(idp_id)
        user_progress = UserProgress(tasks)
        return IDPProgressSchema(
            task_count=user_progress.task_count,
            task_progress=user_progress.progress,
        )

from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import IDPNotFoundError
from app.schemas.idp import IDPCreateSchema, IDPFilter, IDPGetSchema
from database.models.idp import Idp


class AbstractIDPRepository(ABC):
    @abstractmethod
    async def create(self, user_data: IDPCreateSchema) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_and_filter(self, user_id: UUID, filter: IDPFilter) -> IDPGetSchema:
        raise NotImplementedError


class SQLAlchemyIDPRepository(AbstractIDPRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, ipd_data: IDPCreateSchema) -> None:
        idp = Idp(**ipd_data.model_dump())
        self._session.add(idp)
        await self._session.commit()

    async def get_by_user_and_filter(self, user_id: UUID, filter: IDPFilter) -> IDPGetSchema:
        query = select(Idp).where(and_(Idp.user_id == user_id, Idp.year == filter.year))
        result = (await self._session.execute(query)).scalar_one_or_none()
        if not result:
            raise IDPNotFoundError

        return IDPGetSchema.model_validate(result)
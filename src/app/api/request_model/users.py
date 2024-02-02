from enum import StrEnum, auto
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel


class UserSortByEnum(StrEnum):
    family_name = auto()
    task_count = auto()
    task_progress = auto()


class UserOrderEnum(StrEnum):
    asc = auto()
    desc = auto()


class UserQueryParams(BaseModel):
    sort_by: UserSortByEnum = UserSortByEnum.family_name
    order: UserOrderEnum = UserOrderEnum.asc
    team_id: UUID | None = None


UserQueryParamsDep = Annotated[UserQueryParams, Depends()]

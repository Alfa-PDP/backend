from enum import StrEnum
from functools import cached_property
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel


class UserOrderEnum(StrEnum):
    family_name_asc = "family_name,asc"
    family_name_desc = "family_name,desc"
    task_count_asc = "task_count,asc"
    task_count_desc = "task_count,desc"
    task_progress_asc = "task_progress,asc"
    task_progress_desc = "task_progress,desc"

    @cached_property
    def field(self) -> str:
        return self.value.split(",")[0]

    @cached_property
    def is_desc(self) -> bool:
        return self.value.split(",")[1] == "desc"


class UserQueryParams(BaseModel):
    order: UserOrderEnum = UserOrderEnum.family_name_asc
    team_id: UUID | None = None


UserQueryParamsDep = Annotated[UserQueryParams, Depends()]

import datetime
from enum import StrEnum, auto
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query
from pydantic import BaseModel


class UserSortByEnum(StrEnum):
    """
    Перечисление для определения полей, по которым можно сортировать пользователей.
    """

    family_name = auto()
    task_count = auto()
    task_progress = auto()


class UserOrderEnum(StrEnum):
    """
    Перечисление для определения направления сортировки пользователей.
    """

    asc = auto()
    desc = auto()


class UserQueryParams(BaseModel):
    """
    Модель для валидации запроса параметров пользователя.

    Атрибуты:
        - sort_by (UserSortByEnum): Поле для сортировки. По умолчанию - 'family_name'.
        - order (UserOrderEnum): Направление сортировки. По умолчанию - 'asc'.
        - team_id (UUID | None): Идентификатор команды. По умолчанию - None.
        - year (int): Год. По умолчанию - текущий год.
    """

    sort_by: UserSortByEnum = UserSortByEnum.family_name
    order: UserOrderEnum = UserOrderEnum.asc
    team_id: UUID | None = None
    year: int = Query(default=datetime.datetime.now().year)


UserQueryParamsDep = Annotated[UserQueryParams, Depends()]


class UserTasksQueryParams(BaseModel):
    """
    Модель для валидации запроса параметров задач пользователя.

    Атрибуты:
        - year (int): Год. По умолчанию - текущий год.
    """

    year: int = Query(default=datetime.datetime.now().year)


UserTasksQueryParamsDep = Annotated[UserTasksQueryParams, Depends()]

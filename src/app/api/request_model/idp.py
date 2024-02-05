import datetime
from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class IDPQueryParams(BaseModel):
    """
    Модель для валидации запроса параметров ИПР.

    Атрибуты:
        - year (int): Год. По умолчанию - текущий год.
    """

    year: int = Query(default=datetime.datetime.now().year)


IDPQueryParamsDep = Annotated[IDPQueryParams, Depends()]

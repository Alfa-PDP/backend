import datetime
from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class IDPQueryParams(BaseModel):
    year: int = Query(default=datetime.datetime.now().year)


IDPQueryParamsDep = Annotated[IDPQueryParams, Depends()]

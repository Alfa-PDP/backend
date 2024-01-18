from enum import StrEnum, auto
from uuid import UUID

from pydantic import BaseModel


class UserRole(StrEnum):
    employee = auto()
    supervisor = auto()


class UserSchema(BaseModel):
    id: UUID
    name: str
    family_name: str
    surname: str
    position: str
    role: UserRole

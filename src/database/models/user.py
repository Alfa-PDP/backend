from enum import StrEnum, auto

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class UserRole(StrEnum):
    employee = auto()
    supervisor = auto()


class User(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.users db table."""

    __tablename__ = "users"

    name: Mapped[str] = Column(String(64), nullable=False, comment="Имя пользователя")
    family_name: Mapped[str] = Column(String(64), nullable=False, comment="Фамилия пользователя")
    surname: Mapped[str] = Column(String(64), nullable=False, comment="Отчество пользователя")
    position: Mapped[str] = Column(String(64), nullable=False, comment="Должность пользователя")

    role: Mapped[str] = Column(
        ENUM(UserRole, name="user_role"),
        nullable=False,
        comment="Роль пользователя",
        default=UserRole.employee,
        server_default=UserRole.employee,
    )

    def __repr__(self) -> str:
        return f"User({self.id}, {self.name}, {self.family_name}, {self.role}, {self.is_superuser})"

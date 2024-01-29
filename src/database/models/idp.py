from datetime import date

from sqlalchemy import UUID, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class Idp(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "idp"

    user_id: Mapped[UUID] = Column(
        ForeignKey("users.id", name="idp_users_fkey", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Статус выполнения задачи",
    )
    start_date: Mapped[date] = Column(Date, nullable=False, comment="Начало ИПР")
    end_date: Mapped[date] = Column(Date, nullable=False, comment="Окончание ИПР")
    year: Mapped[int] = Column(Integer, nullable=False, comment="Год ИПР")

    def __repr__(self) -> str:
        return f"Idp({self.id}, {self.user_id})"

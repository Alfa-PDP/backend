from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin


class Status(BaseModel, IdMixin):
    __tablename__ = "status"

    slug: Mapped[str] = Column(String(20), nullable=False, comment="Описание на англйском для фронта")
    description: Mapped[str] = Column(String(20), nullable=False, comment="Описание статуса задачи")
    weight: Mapped[int] = Column(Integer(), nullable=False, comment="Вес статуса для сортировки")

    def __repr__(self) -> str:
        return f"Status({self.id}, {self.task_status_description})"

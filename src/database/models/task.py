from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, relationship

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated

if TYPE_CHECKING:
    from database.models.tasknumber import TaskNumber
    from database.models.comment import Comment


class Task(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "tasks"

    name: Mapped[str] = Column(String(100), nullable=False, comment="Наименование задачи")
    description: Mapped[str] = Column(String(1000), nullable=False, comment="Подробности задачи")
    task_type: Mapped[str] = Column(String(20), nullable=False, comment="Тип задачи")
    start_time: Mapped[datetime] = Column(Date, nullable=False, comment="Дата начала")
    end_time: Mapped[datetime] = Column(Date, nullable=False, comment="Дата окончания")
    status_description: Mapped[str] = Column(String(20), nullable=False, comment="Статус выполнения задачи")
    importance: Mapped[str] = Column(String(10), nullable=False, comment="Значимость задачи")

    comments: Mapped[list["Comment"]] = relationship(back_populates="list_of_comments")
    list_of_tasks: Mapped["TaskNumber"] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task({self.id}, {self.task_name})"

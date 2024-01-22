from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, relationship

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated

if TYPE_CHECKING:
    from database.models.tasknumber import Tasknumber


class Task(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "tasks"

    name: Mapped[str] = Column(String(100), nullable=False, comment="Наименование задачи")
    description: Mapped[str] = Column(String, nullable=False, comment="Подробности задачи")
    task_type: Mapped[str] = Column(String(20), nullable=False, comment="Тип задачи")
    start_time: Mapped[datetime] = Column(Date, nullable=False, comment="Дата начала")
    end_time: Mapped[datetime] = Column(Date, nullable=False, comment="Дата окончания")
    status_description: Mapped[str] = Column(String(20), nullable=False, comment="Статус выполнения задачи")
    employee_comment: Mapped[str] = Column(String, comment="Комментарий сотрудника")
    boss_comment: Mapped[str] = Column(String, comment="Комментарий руководтеля")
    importance: Mapped[str] = Column(String(2), nullable=False, comment="Значимость задачи")
    task_id: Mapped[UUID] = Column(
        ForeignKey("task_number.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Порядковый номер в списке задач",
    )

    list_of_tasks: Mapped["Tasknumber"] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task({self.id},{self.task_name})"

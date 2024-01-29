from datetime import date

from sqlalchemy import Date, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class Task(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "tasks"

    name: Mapped[str] = Column(String(100), nullable=False, comment="Наименование задачи")
    description: Mapped[str] = Column(String(1000), nullable=False, comment="Подробности задачи")
    task_type: Mapped[str] = Column(String(20), nullable=False, comment="Тип задачи")
    start_time: Mapped[date] = Column(Date, nullable=False, comment="Дата начала")
    end_time: Mapped[date] = Column(Date, nullable=False, comment="Дата окончания")
    importance: Mapped[str] = Column(String(10), nullable=False, comment="Значимость задачи")
    idp_id: Mapped[UUID] = Column(
        ForeignKey("idp.id", name="task_idp_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Идентифекатор ИПР задачи",
    )
    status_id: Mapped[UUID] = Column(
        ForeignKey("status.id", name="task_status", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Статус выполнения задачи",
    )

    def __repr__(self) -> str:
        return f"Task({self.id}, {self.task_name})"

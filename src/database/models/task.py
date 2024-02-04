from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from database.models.status import Status
from database.models.task_importance import Importance
from database.models.task_type import Type

if TYPE_CHECKING:
    from database.models.comment import Comment
    from database.models.status import Status


class Task(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "tasks"

    name: Mapped[str] = Column(String(100), nullable=False, comment="Наименование задачи")
    description: Mapped[str] = Column(String(1000), nullable=False, comment="Подробности задачи")
    task_type_id: Mapped[UUID] = Column(
        ForeignKey("task_type.id", name="task_type", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Тип задачи",
    )
    start_time: Mapped[date] = Column(Date, nullable=False, comment="Дата начала")
    end_time: Mapped[date] = Column(Date, nullable=False, comment="Дата окончания")
    importance_id: Mapped[UUID] = Column(
        ForeignKey("task_importance.id", name="task_importance", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Значимость задачи",
    )
    idp_id: Mapped[UUID] = Column(
        ForeignKey("idp.id", name="task_idp_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Идентификатор ИПР задачи",
    )
    status_id: Mapped[UUID] = Column(
        ForeignKey("status.id", name="task_status", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Статус выполнения задачи",
    )

    task_type: Mapped["Type"] = relationship()
    importance: Mapped["Importance"] = relationship()
    status: Mapped["Status"] = relationship()
    comments: Mapped[list["Comment"]] = relationship()

    def __repr__(self) -> str:
        return f"Task({self.id}, {self.name})"

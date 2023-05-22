from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities.enums import TaskTypeEnum
from src.domain.entities.base import Base

if TYPE_CHECKING:
    from src.domain.entities.answer import Answer


class Task(Base):
    __tablename__ = "tasks"

    form_id: Mapped[UUID] = mapped_column(ForeignKey("Form.id"), init=False)
    task_content: Mapped[str]
    task_type: Mapped[TaskTypeEnum]
    answers: Mapped[list["Answer"]] = relationship(back_populates="task")

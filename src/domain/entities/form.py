from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities.base import Base

if TYPE_CHECKING:
    from src.domain.entities.task import Task


class Form(Base):
    __tablename__ = "forms"

    name: Mapped[str]
    revision_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("Revision.id"),
        init=False,
    )
    tasks: Mapped[list["Task"]] = relationship()
    is_template: Mapped[bool]

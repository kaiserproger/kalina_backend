from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.domain.entities.base import Base

if TYPE_CHECKING:
    from src.domain.entities.revision import Revision
    from src.domain.entities.enums import MediaEnum


class Attachment(Base):
    __tablename__ = "Attachment"

    revision_id: Mapped[UUID] = mapped_column(ForeignKey("Revision.id"))
    revision: Mapped["Revision"] = relationship()
    media_type: Mapped["MediaEnum"]
    attachment_url: Mapped[str]

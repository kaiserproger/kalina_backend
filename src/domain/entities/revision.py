from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities.base import Base

if TYPE_CHECKING:
    from src.domain.entities.attachment import Attachment
    from src.domain.entities.form import Form


class Revision(Base):
    __tablename__ = "revisions"

    form: Mapped["Form"] = relationship()
    user_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("User.id"),
        nullable=True,
    )
    attachments: Mapped[list["Attachment"]] = relationship(
        back_populates="revision",
    )
    shop_address: Mapped[str]
    expire_date: Mapped[datetime]
    completed: Mapped[bool]
    approved: Mapped[bool]

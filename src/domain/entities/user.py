from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.domain.entities.base import Base

if TYPE_CHECKING:
    from src.domain.entities.revision import Revision

ACTIVE_REVISION_QUERY = "and_(Revision.user_id == User.id, not_(Revision.completed))"


class User(Base):
    __tablename__ = "users"

    phone: Mapped[str] = mapped_column(unique=True, index=True)
    active_revision: Mapped["Revision"] = relationship(
        primaryjoin=ACTIVE_REVISION_QUERY,
        init=False,
    )
    name: Mapped[str]
    admin: Mapped[bool]
    scores: Mapped[int]

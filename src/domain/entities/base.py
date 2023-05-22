from uuid import UUID

from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, Mapped,\
    mapped_column


class Base(DeclarativeBase, MappedAsDataclass):
    id: Mapped[UUID] = mapped_column(primary_key=True, init=False)

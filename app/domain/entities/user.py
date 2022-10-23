from app.domain.entities.revision import Revision
from .base import Base
from app.imports import Column, String, relationship, Boolean


class User(Base):
    __tablename__ = "User"
    phone = Column(String, primary_key=True)
    revision: Revision = relationship(Revision,
                                      primaryjoin="and_(User.phone == Revision.user_id, Revision.completed == False)",
                                      uselist=False)  # type: ignore
    name = Column(String)
    admin = Column(Boolean, default=False)

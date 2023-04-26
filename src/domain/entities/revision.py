from typing import Optional
from uuid import uuid4
from app.domain.entities.attachment import Attachment
from app.domain.entities.form import Form
from .base import Base
from app.imports import Column, ForeignKey, UUID, relationship, String,\
    DateTime, Boolean


class Revision(Base):
    __tablename__ = "Revision"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    form: Form = relationship(Form, uselist=False,
                              cascade="all, delete-orphan")  # type: ignore
    user_id: Optional[str] = Column(ForeignKey("User.phone"),
                                    nullable=True)  # type: ignore
    attachments: list[Attachment] = relationship(Attachment,
                                                 uselist=True,
                                                 cascade="all")  # type: ignore
    shop_address = Column(String)
    expire_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)

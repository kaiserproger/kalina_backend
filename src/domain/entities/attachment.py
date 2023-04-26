from uuid import uuid4
from .base import Base
from src.imports import Column, Enum, String, UUID, ForeignKey
from .enums import MediaEnum


class Attachment(Base):
    __tablename__ = "Attachment"
    revision_id = Column(ForeignKey("Revision.id"))
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    media_type = Column(Enum(MediaEnum, validate_strings=True))
    attachment_url = Column(String)

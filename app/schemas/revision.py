from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from app.schemas.attachment import AttachmentDTO

from .form import FormDTO


class RevisionDTO(BaseModel):
    form: FormDTO
    attachments: list[AttachmentDTO]
    shop_address: str  # Пока без валидации, на потом)))
    name: str
    expire_date: datetime
    active: bool

    class Config:
        orm_mode = True


class CreateRevisionDTO(BaseModel):
    form_template_id: UUID
    shop_address: str
    expire_date: datetime

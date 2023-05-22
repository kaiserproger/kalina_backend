from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.schemas.attachment import AttachmentDto
from src.schemas.form import FormDto


class RevisionDto(BaseModel):
    id: UUID
    form: FormDto
    attachments: list[AttachmentDto]
    shop_address: str  # Пока без валидации, на потом)))
    name: str
    expire_date: datetime
    active: bool

    class Config:
        orm_mode = True


class CreateRevisionDto(BaseModel):
    form_template_id: UUID
    shop_address: str
    expire_date: datetime

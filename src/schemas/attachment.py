from pydantic import BaseModel
from src.domain.entities.enums import MediaEnum


class AttachmentDTO(BaseModel):
    media_type: MediaEnum
    attachment_url: str  # TODO: ВАЛИДАЦИЯ

    class Config:
        orm_mode = True

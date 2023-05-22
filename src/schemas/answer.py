from pydantic import BaseModel


class AnswerDto(BaseModel):
    content: str

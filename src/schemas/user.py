from typing import Optional
from re import search

from pydantic import BaseModel, validator

from src.schemas.revision import RevisionDto


class SignDto(BaseModel):
    phone: str

    @validator('phone')
    def validate_phone(cls, v: str):
        regex = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
        if not search(regex, v):
            raise ValueError("")
        return v.replace("+7", "") if v[0] == "+" else v.replace("8", "")


class VerifyDto(SignDto):
    code: int

    @validator('code')
    def validate_code(cls, v: int):
        if not len(str(v)) == 4:
            raise ValueError("Incorrect code!")
        return v


class RegisterDto(SignDto):
    name: str


class UserDto(RegisterDto):
    scores: int
    revision: Optional[RevisionDto]

    class Config:
        orm_mode = True

from pydantic import BaseModel, validator
from re import search


class SignDTO(BaseModel):
    phone: str

    @validator('phone')
    def validate_phone(cls, v: str):
        regex = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
        if not search(regex, v):
            raise ValueError("")
        return v.replace("+7", "") if v[0] == "+" else v.replace("8", "")


class VerifyDTO(SignDTO):
    code: int

    @validator('code')
    def validate_code(cls, v: int):
        if not len(str(v)) == 4:
            raise ValueError("Incorrect code!")
        return v


class RegisterDTO(SignDTO):
    name: str


class UserDTO(RegisterDTO):
    scores: int

    class Config:
        orm_mode = True

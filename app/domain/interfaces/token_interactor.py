from abc import ABC
from typing import Any
from app.auth.header_extract import HeaderTokenExtractor

from app.auth.jwt import JWTInteractor
from fastapi import Depends


class TokenInteractorProto(ABC):
    def __init__(self, token: str = Depends(HeaderTokenExtractor),
                 jwt_interactor: JWTInteractor = Depends()) -> None:
        ...

    async def validate(self) -> dict[str, Any]:
        ...

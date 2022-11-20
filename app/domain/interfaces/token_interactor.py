from abc import ABC, abstractmethod
from typing import Any
from app.auth.header_extract import HeaderTokenExtractor

from app.auth.jwt import JWTInteractor
from fastapi import Depends


class TokenInteractorProto(ABC):

    @abstractmethod
    def __init__(self, token: str = Depends(HeaderTokenExtractor),
                 jwt_interactor: JWTInteractor = Depends()) -> None:
        ...

    @abstractmethod
    async def validate(self) -> dict[str, Any]:
        ...

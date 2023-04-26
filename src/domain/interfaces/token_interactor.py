from abc import ABC, abstractmethod
from typing import Any
from src.auth.header_extract import HeaderTokenExtractor

from src.auth.jwt import JWTInteractor
from fastapi import Depends


class TokenInteractorProto(ABC):

    @abstractmethod
    def __init__(self, token: str = Depends(HeaderTokenExtractor),
                 jwt_interactor: JWTInteractor = Depends()) -> None:
        ...

    @abstractmethod
    async def validate(self) -> dict[str, Any]:
        ...

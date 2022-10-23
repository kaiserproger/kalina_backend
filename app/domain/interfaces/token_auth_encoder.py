from abc import ABC
from typing import Any

from fastapi import Depends

from app.auth.jwt import JWTInteractor


class TokenAuthEncoderProto(ABC):
    def __init__(self, jwt_interactor: JWTInteractor = Depends()) -> None:
        ...

    async def __call__(self, **kwds: Any) -> str:
        ...

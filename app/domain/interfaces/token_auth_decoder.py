from abc import ABC
from typing import Any
from fastapi import Depends

from .token_interactor import TokenInteractorProto
from .user_repository import UserRepositoryProto


class TokenAuthDecoderProto(ABC):
    def __init__(self, interactor: TokenInteractorProto = Depends(),
                 user_repo: UserRepositoryProto =
                 Depends()) -> None:
        ...

    async def __call__(self) -> Any:
        ...

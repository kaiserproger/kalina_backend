from abc import ABC
from typing import Any
from .token_interactor import TokenInteractorProto
from .user_repository import UserRepositoryProto

from fastapi import Depends


class AdminTokenAuthDecoderProto(ABC):
    def __init__(self, interactor: TokenInteractorProto = Depends(),
                 user_repo: UserRepositoryProto =
                 Depends()) -> None:
        ...

    async def __call__(self) -> Any:
        ...

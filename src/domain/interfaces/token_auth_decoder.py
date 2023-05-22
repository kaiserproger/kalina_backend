from abc import ABC, abstractmethod
from typing import Any
from fastapi import Depends

from .token_interactor import TokenInteractorProto
from .repositories.user_repository import UserRepositoryProto


class TokenAuthDecoderProto(ABC):

    @abstractmethod
    def __init__(self, interactor: TokenInteractorProto = Depends(),
                 user_repo: UserRepositoryProto =
                 Depends()) -> None:
        ...

    @abstractmethod
    async def __call__(self) -> Any:
        ...

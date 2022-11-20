from abc import ABC, abstractmethod
from typing import Any
from .token_interactor import TokenInteractorProto
from .user_repository import UserRepositoryProto

from fastapi import Depends


class AdminTokenAuthDecoderProto(ABC):

    @abstractmethod
    def __init__(self, interactor: TokenInteractorProto = Depends(),
                 user_repo: UserRepositoryProto =
                 Depends()) -> None:
        ...

    @abstractmethod
    async def __call__(self) -> Any:
        ...

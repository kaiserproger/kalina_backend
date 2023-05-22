from abc import ABC, abstractmethod
from ..repositories.user_repository import UserRepositoryProto
from src.domain.entities.user import User

from fastapi import Depends


class UserServiceProto(ABC):

    @abstractmethod
    def __init__(self, user_repo: UserRepositoryProto = Depends()) -> None:
        ...

    @abstractmethod
    async def create_user(self, phone: str, name: str) -> User:
        ...

    @abstractmethod
    async def get_user_by_phone(self, phone: str) -> User:
        ...

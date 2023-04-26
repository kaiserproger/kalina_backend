from abc import ABC, abstractmethod
from .user_repository import UserRepositoryProto
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
    async def is_user_exists(self, phone: str):
        ...

    @abstractmethod
    async def read_by_id(self, phone: str, no_joins: bool) -> User:
        ...

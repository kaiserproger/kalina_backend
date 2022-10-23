from abc import ABC
from .user_repository import UserRepositoryProto
from app.domain.entities.user import User

from fastapi import Depends


class UserServiceProto(ABC):
    def __init__(self, user_repo: UserRepositoryProto = Depends()) -> None:
        ...

    async def create_user(self, phone: str, name: str) -> User:
        ...

    async def is_user_exists(self, phone: str):
        ...

    async def read_by_id(self, phone: str, no_joins: bool) -> User:
        ...

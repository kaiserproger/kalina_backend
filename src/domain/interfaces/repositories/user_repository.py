from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.entities.user import User


class UserRepositoryProto(ABC):
    @abstractmethod
    async def create_user(self, objekt: User):
        ...

    @abstractmethod
    async def update_user(self, objekt: User):
        ...

    @abstractmethod
    async def delete_user(self, id_: UUID) -> None:
        ...

    @abstractmethod
    async def get_user_by_id(self, id_: str, no_joins: bool = False) -> User:
        ...

    @abstractmethod
    async def get_all_users(self, offset: int, limit: int) -> List[User]:
        ...

    @abstractmethod
    async def get_user_by_phone(self, phone: str) -> User:
        ...

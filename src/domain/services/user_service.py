from src.domain.entities.user import User
from domain.interfaces.repositories.user_repository import UserRepositoryProto
from domain.interfaces.services.user_service import UserServiceProto


class UserService(UserServiceProto):
    def __init__(self, user_repo: UserRepositoryProto) -> None:
        self.user_repo = user_repo

    async def create_user(self, phone: str, name: str) -> User:
        user = User(
            phone=phone,
            name=name,
            admin=False,
            scores=0
        )
        await self.user_repo.create_user(user)  # type: ignore
        return await self.user_repo.get_user_by_phone(phone)

    async def get_user_by_phone(self, phone: str, no_joins: bool):
        return await self.user_repo.get_user_by_phone(phone)

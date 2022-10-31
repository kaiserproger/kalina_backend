from app.db.repositories.user_repository import UserRepository
from app.domain.entities.user import User


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def create_user(self, phone: str, name: str) -> User:
        await self.user_repo.\
            create(User(phone=phone, name=name, admin=False, scores=0))  # type: ignore
        return await self.user_repo.read_by_id(phone, True)

    async def is_user_exists(self, phone: str):
        '''It will throw an exception if user is not exist'''
        await self.user_repo.read_by_id(phone, True)

    async def read_by_id(self, phone: str, no_joins: bool):
        return await self.user_repo.read_by_id(phone, no_joins)

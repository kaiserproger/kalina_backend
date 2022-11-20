from app.domain.entities.user import User
from app.domain.interfaces.user_repository import UserRepositoryProto
from app.domain.interfaces.user_service import UserServiceProto


class UserService(UserServiceProto):
    def __init__(self, user_repo: UserRepositoryProto) -> None:
        self.user_repo = user_repo

    async def create_user(self, phone: str, name: str) -> User:
        await self.user_repo.\
            create(User(phone=phone, name=name,
                        admin=False, scores=0))  # type: ignore
        return await self.user_repo.read_by_id(phone, True)

    async def is_user_exists(self, phone: str):
        '''It will throw an exception if user is not exist'''
        await self.user_repo.read_by_id(phone, True)

    async def read_by_id(self, phone: str, no_joins: bool):
        return await self.user_repo.read_by_id(phone, no_joins)

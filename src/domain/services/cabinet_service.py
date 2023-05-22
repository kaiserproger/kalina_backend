from src.domain.entities.user import User
from src.domain.interfaces.services.cabinet_service import CabinetServiceProto
from src.domain.interfaces.repositories.\
    user_repository import UserRepositoryProto
from src.schemas.user import UserDto


class CabinetService(CabinetServiceProto):
    def __init__(self, user_repo: UserRepositoryProto) -> None:
        self.user_repo = user_repo

    async def get_user_cabinet(self, user: User) -> UserDto:
        return UserDto.from_orm(
            await self.user_repo.get_user_by_phone(user.phone)
        )

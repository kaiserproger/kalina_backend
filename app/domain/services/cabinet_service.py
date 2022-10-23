from app.db.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.schemas.user import UserDTO


class CabinetService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def get_user_cabinet(self, user: User) -> UserDTO:
        return UserDTO.from_orm(await self.user_repo.
                                read_by_id(user.phone))  # type: ignore

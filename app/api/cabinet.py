from fastapi import APIRouter, Depends
from app.domain.entities.user import User
from app.domain.interfaces.cabinet_service import CabinetServiceProto
from app.exceptions.invalid_token import InvalidTokenException
from app.schemas.user import UserDTO


cabinet_router = APIRouter(prefix="/cabinet")


@cabinet_router.get("/", responses={
    200: {"description": "Returning Cabinet"}
})
async def get_cabinet(cabinet_service: CabinetServiceProto = Depends(),
                      user: User = Depends()) -> UserDTO:
    if not user.admin:
        raise InvalidTokenException("Access denied")
    return await cabinet_service.get_user_cabinet(user)

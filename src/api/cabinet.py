from fastapi import APIRouter, Depends
from src.domain.entities.user import User
from src.domain.interfaces.cabinet_service import CabinetServiceProto
from src.exceptions.invalid_token import InvalidTokenException
from src.schemas.user import UserDTO


cabinet_router = APIRouter(prefix="/cabinet")


@cabinet_router.get("/", responses={
    200: {"description": "Returning Cabinet"}
})
async def get_cabinet(cabinet_service: CabinetServiceProto = Depends(),
                      user: User = Depends()) -> UserDTO:
    return await cabinet_service.get_user_cabinet(user)

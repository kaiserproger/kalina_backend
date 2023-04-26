from fastapi import APIRouter, Depends
from src.di.di_stubs import user_stub
from src.domain.entities.user import User
from src.domain.interfaces.cabinet_service import CabinetServiceProto
from src.schemas.user import UserDTO


cabinet_router = APIRouter(prefix="/cabinet")


@cabinet_router.get("/", responses={
    200: {"description": "Returning Cabinet"}
})
async def get_cabinet(
    cabinet_service: CabinetServiceProto = Depends(),
    user: User = Depends(user_stub)
) -> UserDTO:
    return await cabinet_service.get_user_cabinet(user)

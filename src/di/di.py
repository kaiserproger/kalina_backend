from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.di.di_stubs import get_session_stub
from src.domain.interfaces.token_auth_decoder import TokenAuthDecoderProto
from src.domain.interfaces.repositories.\
    user_repository import UserRepositoryProto
from src.domain.interfaces.repositories.\
    form_repository import FormRepositoryProto
from src.domain.interfaces.repositories.\
    revision_repository import RevisionRepositoryProto
from src.domain.services.form_service import FormService
from src.domain.services.user_service import UserService
from src.db.repositories.user_repository import UserRepository
from src.db.repositories.form_repository import FormRepository
from src.db.repositories.revision_repository import RevisionRepository
from src.domain.services.cabinet_service import CabinetService
from src.domain.services.revision_service import RevisionService


async def get_user_repository(
    session: AsyncSession = Depends(get_session_stub),
):
    return UserRepository(session)


async def get_form_repository(
    session: AsyncSession = Depends(get_session_stub),
):
    return FormRepository(session)


async def get_revision_repository(
    session: AsyncSession = Depends(get_session_stub),
):
    return RevisionRepository(session)


async def get_cabinet_service(user_repo: UserRepositoryProto = Depends()):
    return CabinetService(user_repo)


async def get_revision_service(
    user_repo: UserRepositoryProto = Depends(),
    form_repo: FormRepositoryProto = Depends(),
    revision_repo: RevisionRepositoryProto = Depends(),
):
    return RevisionService(revision_repo, form_repo, user_repo)


async def get_user_service(user_repo: UserRepositoryProto = Depends()):
    return UserService(user_repo)


async def get_form_service(form_repo: FormRepositoryProto = Depends()):
    return FormService(form_repo)


async def extract_user(decoder: TokenAuthDecoderProto = Depends()):
    return await decoder()

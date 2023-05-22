from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Response, Path

from src.di.di_stubs import user_stub
from src.domain.interfaces.\
    admin_token_decoder import AdminTokenAuthDecoderProto
from src.domain.entities.user import User
from domain.interfaces.services.revision_service import RevisionServiceProto
from src.schemas.attachment import AttachmentDto
from src.schemas.form import FormDto
from src.schemas.revision import CreateRevisionDto, RevisionDto


revision_router = APIRouter(prefix="/revision")


@revision_router.get("/", responses={
    200: {"description": ""},
    404: {"description": "No revision selected!"},
})
async def get_current_revision(
    user: User = Depends(user_stub),
    rev_service: RevisionServiceProto = Depends(),
) -> RevisionDto:
    return RevisionDto.from_orm((await rev_service.get_user_revision(user)))


@revision_router.get("/available")
async def get_revisions_available(
    service: RevisionServiceProto = Depends(),
)-> List[RevisionDto]:
    return await service.get_available_revisions()


@revision_router.post("/", responses={
    201: {"description": ""},
    400: {"description": "Not an admin"}
}, dependencies=[Depends(AdminTokenAuthDecoderProto)])
async def create_revision(
    dto: CreateRevisionDto,
    response: Response,
    service: RevisionServiceProto = Depends(),
) -> None:
    await service.create_revision(dto.form_template_id, dto.shop_address,
                                  dto.expire_date)
    response.status_code = 201


@revision_router.put("/", responses={
    200: {"description": "Added"},
})
async def update_revision(
    attachments: list[AttachmentDto],
    user: User = Depends(user_stub),
) -> None:
    ...


@revision_router.post("/complete")
async def complete_revision(
    user: User = Depends(user_stub),
    service: RevisionServiceProto = Depends(),
) -> None:
    await service.complete_revision(user)


@revision_router.post("/select/{revision_id}")
async def select_revision(
    revision_id: UUID = Path(),
    user: User = Depends(user_stub),
    service: RevisionServiceProto = Depends(),
) -> None:
    await service.select_revision(user, revision_id)


@revision_router.post(
    "/approve/{revision_id}",
    dependencies=[Depends(AdminTokenAuthDecoderProto)]
)
async def approve_revision(
    revision_id: UUID = Path(),
    service: RevisionServiceProto = Depends(),
) -> None:
    await service.approve_revision(revision_id)


@revision_router.post("/revision/form", responses={
    200: {"description": "Form succesfully uploaded"},

})
async def update_revision_form(
    form: FormDto,
    user: User = Depends(user_stub),
    service: RevisionServiceProto = Depends()
) -> None:
    await service.update_revision_form(user, form)

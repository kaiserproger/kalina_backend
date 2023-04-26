from typing import List
from uuid import UUID
from fastapi import APIRouter
from src.domain.interfaces.admin_token_decoder import AdminTokenAuthDecoderProto
from src.domain.interfaces.form_service import FormServiceProto
from src.schemas.form import FormDTO

from src.schemas.task import TaskDTO

from fastapi import Depends


template_router = APIRouter(prefix="/template")


@template_router.post("/", dependencies=[Depends(AdminTokenAuthDecoderProto)])
async def create_template(tasks: list[TaskDTO],
                          name: str,
                          form_service: FormServiceProto = Depends()):
    await form_service.create_template(tasks, name)


@template_router.get("/")
async def get_templates(form_service: FormServiceProto =
                        Depends()) -> List[FormDTO]:
    return await form_service.get_templates()


@template_router.get("/{form_id}")
async def get_template(template_id: UUID,
                       form_service: FormServiceProto =
                       Depends()) -> FormDTO:
    return await form_service.get_template(template_id)

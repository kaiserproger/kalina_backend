from uuid import UUID
from typing import Any, List, cast

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.entities.form import Form
from src.domain.entities.task import Task
from domain.interfaces.repositories.form_repository import FormRepositoryProto
from src.exceptions.not_found import NotFoundException


class FormRepository(FormRepositoryProto):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_form(self, form: Form):
        self.session.add(form)
        await self.session.flush()

    async def update_form(self, objekt: Form, fields: dict[str, Any]):
        statement = update(Form).where()
        await self.session.execute(statement)

    async def delete_form(self, id_: UUID) -> None:
        statement = delete(Form).where(Form.id == id_)
        await self.session.execute(statement)

    async def get_form_by_id(self, id_: UUID) -> Form:
        form = await self.session.get(Form, id_)
        if form is None:
            raise NotFoundException()
        return form

    async def get_all_forms(self, offset: int, limit: int) -> List[Form]:
        query = select(Form).offset(offset).limit(limit)
        forms = (await self.session.execute(query)).scalars().all()
        return cast(list[Form], forms)

    async def get_template_forms(self) -> List[Form]:
        query = select(Form).where(Form.is_template).options(
            selectinload(Form.tasks)
        )
        templates = (await self.session.execute(query)).scalars().all()
        return cast(list[Form], templates)

    async def create_form_from_template(self, template: Form) -> Form:
        form_tasks = [Task(
            task_content=i.task_content,
            task_type=i.task_type,
            answers=i.answers
        ) for i in template.tasks]
        form = Form(name=template.name, is_template=False, tasks=form_tasks)
        self.session.add(form)
        await self.session.flush()
        return form

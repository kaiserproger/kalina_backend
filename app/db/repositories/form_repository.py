from uuid import UUID
from app.domain.entities.form import Form
from app.domain.entities.task import Task
from app.domain.interfaces.base_repository import BaseRepository
from app.exceptions.not_found import NotFoundException
from app.imports import AsyncSession, update, delete, select, eagerload
from typing import Any, List


class FormRepository(BaseRepository[Form]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Form)

    async def create(self, form: Form):
        self.session.add(form)
        await self.session.flush()

    async def update(self, objekt: Form, fields: dict[str, Any]):
        statement = update(Form).where()
        await self.session.execute(statement)

    async def delete(self, id_: UUID) -> None:
        statement = delete(Form).where(Form.id == id_)
        await self.session.execute(statement)

    async def read_by_id(self, id_: UUID) -> Form:
        form = await self.session.get(Form, id_)
        if form is None:
            raise NotFoundException()
        return form

    async def read_multi(self, offset: int, limit: int) -> List[Form]:
        return (await self.session.execute(select(Form).offset(offset).
                limit(limit))).scalars().all()

    async def get_templates(self) -> List[Form]:
        return (await self.session.
                execute(select(Form).
                        where(Form.is_template == True).
                        options(eagerload(Form.tasks)))).scalars().all()

    async def create_from_template(self, template: Form) -> Form:
        form = Form(name=template.name, is_template=False)  # type: ignore
        for i in template.tasks:
            form.tasks.append(Task(task_content=i.task_content,
                                   task_type=i.task_type,
                                   answers=i.answers))  # type: ignore
        self.session.add(form)
        await self.session.flush()
        return form

from uuid import UUID
from app.domain.entities.task import Task
from app.domain.entities.form import Form
from app.db.repositories.form_repository import FormRepository
from app.schemas.form import FormDTO
from app.schemas.task import TaskDTO


class FormService:
    def __init__(self, form_repo: FormRepository):
        self.form_repo = form_repo

    async def create_template(self, tasks: list[TaskDTO], name: str):
        form = Form(name=name, is_template=True)  # type: ignore
        for task in tasks:
            form.tasks.append(Task(task_content=task.task_content,
                                   task_type=task.task_type,
                                   answers=task.answer))  # type: ignore
        await self.form_repo.create(form)

    async def get_templates(self):
        return list(map(lambda model: FormDTO.from_orm(model),
                    (await self.form_repo.get_templates())))

    async def get_template(self, template_id: UUID):
        return FormDTO.from_orm(await self.form_repo.read_by_id(template_id))

from uuid import UUID
from domain.entities.answer import Answer
from src.domain.entities.task import Task
from src.domain.entities.form import Form
from domain.interfaces.repositories.form_repository import FormRepositoryProto
from domain.interfaces.services.form_service import FormServiceProto
from src.schemas.form import FormDto
from src.schemas.task import TaskDto


class FormService(FormServiceProto):
    def __init__(self, form_repo: FormRepositoryProto):
        self.form_repo = form_repo

    async def create_template(self, tasks: list[TaskDto], name: str):
        form = Form(name=name, is_template=True, tasks=[])
        for task in tasks:
            answers = [Answer(content=i.content) for i in task.answers]
            task_ = Task(
                task_content=task.task_content,
                task_type=task.task_type,
                answers=answers,
            )
            form.tasks.append(task_)
        await self.form_repo.create_form(form)

    async def get_templates(self):
        templates = await self.form_repo.get_template_forms()
        return list(map(lambda model: FormDto.from_orm(model), templates))

    async def get_template(self, template_id: UUID):
        return FormDto.from_orm(
            await self.form_repo.get_form_by_id(template_id)
        )

from src.models.task import Task
from src.entities.task import (
    TaskCreateClient,
    TaskCreateDB,
    TaskInfoUpdate,
    TaskStatusUpdate,
)
from src.exceptions.exceptions import ItemAlreadyExist, ItemNotExist

from datetime import date


class TaskService:
    def __init__(self, query, command):
        self._query = query
        self._command = command

    async def _check_task_not_exist(self, user_id, title):
        task = await self._query.get_by_user_and_title(user_id, title)
        if task:
            raise ItemAlreadyExist

    async def get_task(self, user_id: int, task_id: int) -> Task:
        task = await self._query.get_by_user_and_id(user_id, task_id)
        if not task:
            raise ItemNotExist
        return task

    async def get_all_tasks(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        search_query: str | None = None,
        completed: bool | None = None,
        task_date: date | None = None,
        task_type: list[str] | None = None,
    ) -> list[Task]:
        """Фильтрация, пагинация задач"""
        return await self._query.get_all_tasks(
            user_id=user_id,
            skip=skip,
            limit=limit,
            search_query=search_query,
            completed=completed,
            task_date=task_date,
            task_type=task_type,
        )

    async def create_task(
        self, user_id: int, type_id: int, data: TaskCreateClient
    ) -> Task:
        await self._check_task_not_exist(user_id, data.title)
        task_data = TaskCreateDB(
            title=data.title,
            description=data.description,
            task_date=data.task_date,
            user_id=user_id,
            type_id=type_id,
        )
        return await self._command.create(task_data)

    async def delete_task(self, user_id: int, task_id: int) -> dict:
        task = await self.get_task(user_id, task_id)
        await self._command.delete_task(task)
        return {"detail": "Задача успешно удалена!"}

    async def update_task(
        self, user_id: int, task_id: int, data: TaskInfoUpdate
    ) -> Task:
        task = await self._query.get_by_user_and_id(user_id, task_id)
        return await self._command.update(task, data)

    async def task_status_update(
        self, user_id: int, task_id: int, data: TaskStatusUpdate
    ) -> Task:
        task = await self.get_task(user_id, task_id)
        return await self._command.status_update(task, data)

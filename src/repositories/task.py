from src.repositories.base import BaseQueryRepository, BaseCommandRepository
from src.models.task import Task
from src.models.type import TaskType
from src.entities.task import TaskCreateDB, TaskStatusUpdate

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from datetime import date, datetime, timezone


class TaskQueryRepository(BaseQueryRepository[Task]):
    def __init__(self, session):
        super().__init__(session, Task)

    async def get_by_user_and_title(self, user_id: int, title: str) -> Task | None:
        stmt = (
            select(Task)
            .where(and_(Task.user_id == user_id, Task.title == title))
            .options(joinedload(Task.type))
        )
        task = await self._session.execute(stmt)
        return task.scalar_one_or_none()

    async def get_by_user_and_id(self, user_id: int, task_id: int) -> Task | None:
        stmt = (
            select(Task)
            .where(and_(Task.user_id == user_id, Task.id == task_id))
            .options(joinedload(Task.type))
        )
        task = await self._session.execute(stmt)
        return task.scalar_one_or_none()

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
        stmt = (
            select(Task).where(Task.user_id == user_id).options(joinedload(Task.type))
        )

        if task_date is None:
            task_date = date.today()
        stmt = stmt.where(Task.task_date == task_date)
        if search_query:
            stmt = stmt.where(Task.title.ilike(f"%{search_query}%"))
        if completed is not None:
            stmt = stmt.where(Task.completed == completed)
        if task_type:
            stmt = stmt.join(Task.type).where(TaskType.title.in_(task_type))

        stmt = stmt.offset(skip).limit(limit)
        tasks = await self._session.execute(stmt)
        return tasks.scalars().all()


class TaskCommandRepository(BaseCommandRepository[Task, TaskCreateDB]):
    def __init__(self, session):
        super().__init__(session, Task)

    async def delete_task(self, task: Task):
        try:
            await self._session.delete(task)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise

    async def status_update(self, task: Task, data: TaskStatusUpdate) -> Task:
        try:
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(task, key, value)

            if task.completed is True:
                task.completed_at = datetime.now(timezone.utc)
            else:
                task.completed_at = None
            await self._commit(task)
            return task
        except Exception:
            await self._session.rollback()
            raise

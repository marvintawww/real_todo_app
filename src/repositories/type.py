from src.repositories.base import BaseQueryRepository, BaseCommandRepository
from src.models.type import TaskType
from src.entities.type import TaskTypeCreateDB

from sqlalchemy import select, and_


class TypeQueryRepository(BaseQueryRepository[TaskType]):
    def __init__(self, session):
        super().__init__(session, TaskType)

    async def get_by_user_and_title(self, user_id: int, title: str) -> TaskType | None:
        stmt = select(TaskType).where(
            and_(TaskType.user_id == user_id, TaskType.title == title)
        )
        task_type = await self._session.execute(stmt)
        return task_type.scalar_one_or_none()

    async def get_by_user_and_id(self, user_id: int, type_id: int) -> TaskType | None:
        stmt = select(TaskType).where(
            and_(TaskType.user_id == user_id, TaskType.id == type_id)
        )
        task_type = await self._session.execute(stmt)
        return task_type.scalar_one_or_none()

    async def get_all_types(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> list[TaskType]:
        stmt = select(TaskType).where(TaskType.user_id == user_id)
        stmt = stmt.offset(skip).limit(limit)
        types = await self._session.execute(stmt)
        return types.scalars().all()


class TypeCommandRepository(BaseCommandRepository[TaskType, TaskTypeCreateDB]):
    def __init__(self, session):
        super().__init__(session, TaskType)

from src.services.task import TaskService
from src.repositories.task import TaskQueryRepository, TaskCommandRepository
from src.database.db import db

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_task_service(
    session: AsyncSession = Depends(db.get_session),
) -> TaskService:
    return TaskService(
        query=TaskQueryRepository(session), command=TaskCommandRepository(session)
    )

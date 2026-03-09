from src.services.type import TypeService
from src.repositories.type import TypeQueryRepository, TypeCommandRepository
from src.database.db import db

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_type_service(
    session: AsyncSession = Depends(db.get_session),
) -> TypeService:
    return TypeService(
        query=TypeQueryRepository(session), command=TypeCommandRepository(session)
    )

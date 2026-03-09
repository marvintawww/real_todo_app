from src.services.jwt import JWTService
from src.repositories.jwt import JWTQueryRepository, JWTCommandRepository
from src.database.db import db
from src.core.token import JWTProcessor

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_jwt_service(
    session: AsyncSession = Depends(db.get_session),
) -> JWTService:
    return JWTService(
        query=JWTQueryRepository(session),
        command=JWTCommandRepository(session),
        jwt_processor=JWTProcessor(),
    )

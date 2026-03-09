from src.services.user import UserService
from src.repositories.user import UserQueryRepository, UserCommandRepository
from src.utils.security import PasswordHasher
from src.database.db import db

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_service(session: AsyncSession = Depends(db.get_session)):
    return UserService(
        query=UserQueryRepository(session),
        command=UserCommandRepository(session),
        pw_hasher=PasswordHasher(),
    )

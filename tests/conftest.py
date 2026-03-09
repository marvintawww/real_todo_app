import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.database.db import Base
from src.models.user import User
from src.models.jwt import JWTBlacklist
from src.models.task import Task
from src.models.type import TaskType


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    await session.close()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

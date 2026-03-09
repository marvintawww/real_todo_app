import pytest_asyncio

from src.database.db import Base
from src.models.user import User
from src.models.jwt import JWTBlacklist
from src.models.task import Task
from src.models.type import TaskType

from src.repositories.user import UserCommandRepository
from src.repositories.type import TypeCommandRepository
from src.repositories.task import TaskCommandRepository
from src.repositories.jwt import JWTCommandRepository
from src.entities.user import UserCreateDB
from src.entities.type import TaskTypeCreateDB
from src.entities.task import TaskCreateDB
from src.entities.jwt import JWTBlacklistItemCreate


@pytest_asyncio.fixture
async def created_user(db_session):
    command_repo = UserCommandRepository(session=db_session)
    user_data = UserCreateDB(login="alena", hashed_password="alena")
    return await command_repo.create(user_data)


@pytest_asyncio.fixture
async def created_type(db_session):
    command_repo = TypeCommandRepository(session=db_session)
    type_data = TaskTypeCreateDB(title="task_type", user_id=1)
    return await command_repo.create(type_data)


@pytest_asyncio.fixture
async def created_task(db_session):
    command_repo = TaskCommandRepository(session=db_session)
    task_data = TaskCreateDB(
        title="Task", description="Description", type_id=1, user_id=1
    )
    return await command_repo.create(task_data)


@pytest_asyncio.fixture
async def created_jwtblacklist_item(db_session):
    command_repo = JWTCommandRepository(session=db_session)
    jwt_data = JWTBlacklistItemCreate(jti="124")
    return await command_repo.create(jwt_data)

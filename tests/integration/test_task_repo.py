from datetime import date

from src.repositories.task import TaskQueryRepository, TaskCommandRepository
from src.entities.task import TaskCreateDB, TaskInfoUpdate


async def test_create_and_get_task_by_id(db_session):
    command_repo = TaskCommandRepository(session=db_session)
    query_repo = TaskQueryRepository(session=db_session)
    task_data = TaskCreateDB(
        title="Task", description="Description", user_id=1, type_id=1
    )
    task = await command_repo.create(task_data)
    found = await query_repo.get_by_id(task.id)

    assert found is not None
    assert found.title == "Task"
    assert found.description == "Description"
    assert found.task_date == date.today()
    assert found.user_id == 1
    assert found.type_id == 1


async def test_create_task_with_custom_date(db_session):
    command_repo = TaskCommandRepository(session=db_session)
    query_repo = TaskQueryRepository(session=db_session)
    task_data = TaskCreateDB(
        title="Task",
        description="Description",
        task_date="2026-04-09",
        user_id=1,
        type_id=1,
    )
    task = await command_repo.create(task_data)
    found = await query_repo.get_by_id(task.id)

    assert found is not None
    assert found.task_date == date(2026, 4, 9)


async def test_get_task_by_user_and_title(db_session, created_user, created_task):
    query_repo = TaskQueryRepository(session=db_session)
    found = await query_repo.get_by_user_and_title(created_user.id, created_task.title)

    assert found.title == "Task"
    assert found.user_id == 1


async def test_delete_task(db_session, created_task):
    query_repo = TaskQueryRepository(session=db_session)
    command_repo = TaskCommandRepository(session=db_session)
    await command_repo.delete_task(created_task)
    found = await query_repo.get_by_id(created_task.id)

    assert found is None


async def test_update_task(db_session, created_task):
    query_repo = TaskQueryRepository(session=db_session)
    command_repo = TaskCommandRepository(session=db_session)
    new_data = TaskInfoUpdate(
        title="New", description="New desc", completed=True, task_date="2026-09-12"
    )
    updated_task = await command_repo.update(created_task, new_data)
    found = await query_repo.get_by_id(updated_task.id)

    assert found.id == 1
    assert found.title == "New"
    assert found.description == "New desc"
    assert found.completed is True
    assert found.task_date == date(2026, 9, 12)

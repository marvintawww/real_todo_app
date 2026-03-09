from src.repositories.type import TypeCommandRepository, TypeQueryRepository
from src.entities.type import TaskTypeCreateDB


async def test_create_and_get_type_by_id(db_session):
    command_repo = TypeCommandRepository(session=db_session)
    query_repo = TypeQueryRepository(session=db_session)
    type_data = TaskTypeCreateDB(title="task_type", user_id=1)
    task_type = await command_repo.create(type_data)
    found = await query_repo.get_by_id(task_type.id)

    assert found is not None
    assert found.title == "task_type"
    assert found.user_id == 1


async def test_get_type_by_user_and_title(db_session, created_type):
    query_repo = TypeQueryRepository(session=db_session)
    found = await query_repo.get_by_user_and_title(
        created_type.user_id, created_type.title
    )

    assert found.user_id == 1
    assert found.title == "task_type"

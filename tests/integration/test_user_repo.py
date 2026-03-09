import pytest

from src.repositories.user import UserQueryRepository, UserCommandRepository
from src.entities.user import UserCreateDB, UserLoginUpdate, UserStatusUpdate


async def test_create_and_get_user_by_id(db_session):
    query_repo = UserQueryRepository(session=db_session)
    command_repo = UserCommandRepository(session=db_session)
    user_data = UserCreateDB(login="alena", hashed_password="popina")
    user = await command_repo.create(user_data)
    found = await query_repo.get_by_id(user.id)

    assert found is not None
    assert found.id == 1
    assert found.login == "alena"
    assert found.hashed_password is not None


async def test_get_user_by_id_not_found(db_session):
    query_repo = UserQueryRepository(session=db_session)
    found = await query_repo.get_by_id(999)

    assert found is None


async def test_get_user_by_login(db_session, created_user):
    query_repo = UserQueryRepository(session=db_session)
    found = await query_repo.get_by_login(created_user.login)

    assert found.login == "alena"


async def test_create_user_duplicate_login(db_session):
    command_repo = UserCommandRepository(session=db_session)
    user_data = UserCreateDB(login="alena", hashed_password="alena")
    await command_repo.create(user_data)

    with pytest.raises(Exception):
        await command_repo.create(user_data)


async def test_update_user_login(db_session, created_user):
    command_repo = UserCommandRepository(session=db_session)
    update_data = UserLoginUpdate(login="dima")
    upd_user = await command_repo.update(created_user, update_data)

    assert upd_user.login == "dima"


async def test_update_user_status(db_session, created_user):
    command_repo = UserCommandRepository(session=db_session)
    update_data = UserStatusUpdate(is_active=False)
    upd_user = await command_repo.update(created_user, update_data)

    assert upd_user.is_active is False

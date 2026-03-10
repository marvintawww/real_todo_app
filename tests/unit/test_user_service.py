import pytest
from unittest.mock import MagicMock

from src.entities.user import UserCreateClient, UserLoginUpdate
from src.exceptions.exceptions import ItemAlreadyExist, ItemNotExist


async def test_create_user_success(user_service):
    user_service._query.get_by_login.return_value = None
    user_service._command.create.return_value = MagicMock(id=1, login="alena")
    result = await user_service.create_user(
        UserCreateClient(login="alena", password="123")
    )

    assert result.id == 1
    assert result.login == "alena"

    user_service._command.create.assert_called_once()


async def test_create_user_error(user_service):
    user_service._query.get_by_login.return_value = MagicMock(id=1, login="alena")

    with pytest.raises(ItemAlreadyExist):
        await user_service.create_user(UserCreateClient(login="alena", password="123"))


async def test_get_user_by_id_success(user_service):
    user_service._query.get_by_id.return_value = MagicMock(
        id=1, login="alena", is_active=True
    )
    result = await user_service.get_user(1)
    assert result.id == 1


async def test_get_user_by_id_not_found(user_service):
    user_service._query.get_by_id.return_value = None
    with pytest.raises(ItemNotExist):
        await user_service.get_user(1)


async def test_get_user_by_id_inactive(user_service):
    user_service._query.get_by_id.return_value = MagicMock(
        id=1, login="alena", is_active=False
    )
    with pytest.raises(ItemNotExist):
        await user_service.get_user(1)


async def test_update_user_success(user_service):
    pass

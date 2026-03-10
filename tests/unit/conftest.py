import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.user import UserService


@pytest.fixture
def user_service():
    query = AsyncMock()
    command = AsyncMock()
    pw_hasher = MagicMock()
    pw_hasher.hash_pw.return_value = "fake_hash"
    return UserService(query=query, command=command, pw_hasher=pw_hasher)

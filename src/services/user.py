from src.entities.user import (
    UserCreateClient,
    UserLoginUpdate,
    UserStatusUpdate,
    UserCreateDB,
    UserAuthenticate,
)
from src.models.user import User
from src.exceptions.exceptions import ItemAlreadyExist, ItemNotExist, AuthenticateError

from typing import Union


class UserService:
    def __init__(self, query, command, pw_hasher):
        self._query = query
        self._command = command
        self._pw_hasher = pw_hasher

    async def _check_user_not_exist(self, login: int):
        user = await self._query.get_by_login(login)
        if user:
            raise ItemAlreadyExist

    async def get_user(self, user_id: int) -> User:
        user = await self._query.get_by_id(user_id)
        if not user or user.is_active is False:
            raise ItemNotExist
        return user

    async def create_user(self, data: UserCreateClient) -> User:
        await self._check_user_not_exist(data.login)
        hashed_password = self._pw_hasher.hash_pw(data.password)
        user_data = UserCreateDB(login=data.login, hashed_password=hashed_password)
        return await self._command.create(user_data)

    async def update_user(
        self, user_id: int, data: Union[UserStatusUpdate, UserLoginUpdate]
    ) -> User:
        user = await self.get_user(user_id)
        return await self._command.update(user, data)

    async def authenticate(self, data: UserAuthenticate) -> User:
        user = await self._query.get_by_login(data.login)
        if not user:
            raise ItemNotExist
        if not self._pw_hasher.verify(data.password, user.hashed_password):
            raise AuthenticateError
        return user

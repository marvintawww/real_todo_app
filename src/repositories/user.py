from src.repositories.base import BaseQueryRepository, BaseCommandRepository
from src.models.user import User
from src.entities.user import UserCreateDB

from sqlalchemy import select


class UserQueryRepository(BaseQueryRepository[User]):
    def __init__(self, session):
        super().__init__(session, User)

    async def get_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        user = await self._session.execute(stmt)
        return user.scalar_one_or_none()


class UserCommandRepository(BaseCommandRepository[User, UserCreateDB]):
    def __init__(self, session):
        super().__init__(session, User)

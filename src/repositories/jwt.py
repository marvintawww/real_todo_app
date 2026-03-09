from src.repositories.base import BaseQueryRepository, BaseCommandRepository
from src.models.jwt import JWTBlacklist
from src.entities.jwt import JWTBlacklistItemCreate

from sqlalchemy import select


class JWTQueryRepository(BaseQueryRepository[JWTBlacklist]):
    def __init__(self, session):
        super().__init__(session, JWTBlacklist)

    async def get_by_jti(self, jti: str) -> JWTBlacklist | None:
        stmt = select(JWTBlacklist).where(JWTBlacklist.jti == jti)
        jwt = await self._session.execute(stmt)
        return jwt.scalar_one_or_none()


class JWTCommandRepository(BaseCommandRepository[JWTBlacklist, JWTBlacklistItemCreate]):
    def __init__(self, session):
        super().__init__(session, JWTBlacklist)

from uuid import uuid4
from datetime import datetime, timezone, timedelta

from src.config import SECRET
from src.entities.jwt import TokenPairResponse, JWTBlacklistItemCreate
from src.exceptions.exceptions import ItemAlreadyExist

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


class JWTService:
    def __init__(self, query, command, jwt_processor):
        self._query = query
        self._command = command
        self._jwt_processor = jwt_processor

    async def _create_access_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "type": "access",
            "jti": str(uuid4()),
        }
        return await self._jwt_processor.encode(payload, SECRET)

    async def _create_refresh_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "type": "refresh",
            "jti": str(uuid4()),
        }
        return await self._jwt_processor.encode(payload, SECRET)

    async def _check_token_not_in_blacklist(self, jti: str):
        is_blacklisted = await self._query.get_by_jti(jti)
        if is_blacklisted:
            raise ItemAlreadyExist

    async def _add_token_to_blacklist(self, token: str) -> dict:
        payload = await self._jwt_processor.decode(token, SECRET)
        jti = await self._jwt_processor.get_field(payload, "jti")
        await self._check_token_not_in_blacklist(jti)
        return await self._command.create(JWTBlacklistItemCreate(jti=jti))

    async def create_token_pair(self, user_id: int) -> TokenPairResponse:
        return TokenPairResponse(
            access_token=await self._create_access_token(user_id),
            refresh_token=await self._create_refresh_token(user_id),
        )

    async def refresh(self, refresh_token: str):
        await self._add_token_to_blacklist(refresh_token)
        payload = await self._jwt_processor.decode(refresh_token, SECRET)
        user_id = int(await self._jwt_processor.get_field(payload, "sub"))
        return await self.create_token_pair(user_id)

    async def logout(self, refresh_token: str):
        return await self._add_token_to_blacklist(refresh_token)

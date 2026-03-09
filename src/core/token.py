from abc import ABC, abstractmethod
from jose import jwt, JWTError


class TokenProcessor(ABC):
    @abstractmethod
    async def encode(self, payload: dict, secret: str) -> str:
        pass

    @abstractmethod
    async def decode(self, token: str, secret: str) -> dict:
        pass


class JWTProcessor(TokenProcessor):
    async def encode(self, payload: dict, secret: str) -> str:
        try:
            return jwt.encode(payload, secret, algorithm="HS256")
        except JWTError:
            raise

    async def decode(self, token: str, secret: str) -> dict:
        try:
            return jwt.decode(token, secret, algorithms=["HS256"])
        except JWTError:
            raise

    async def get_field(self, payload: dict, field: str):
        res = payload.get(field)
        if not res:
            raise JWTError
        return res

    async def check_token_type(self, payload: dict, type: str):
        if await self.get_field(payload, "type") != type:
            raise JWTError

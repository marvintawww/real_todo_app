from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from src.core.token import JWTProcessor
from src.config import SECRET

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/")
jwt_processor = JWTProcessor()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = await jwt_processor.decode(token, SECRET)
    await jwt_processor.check_token_type(payload, "access")
    return payload

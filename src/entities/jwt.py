from pydantic import BaseModel, ConfigDict


class JWTBlacklistItemCreate(BaseModel):
    jti: str


class TokenPairResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

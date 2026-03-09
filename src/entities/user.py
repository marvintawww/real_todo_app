from pydantic import BaseModel, ConfigDict


class UserCreateClient(BaseModel):
    login: str
    password: str


class UserCreateDB(BaseModel):
    login: str
    hashed_password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login: str


class UserLoginUpdate(BaseModel):
    login: str | None = None


class UserStatusUpdate(BaseModel):
    is_active: bool | None = None


class UserAuthenticate(BaseModel):
    login: str
    password: str

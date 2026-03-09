from pydantic import BaseModel, ConfigDict


class TaskTypeCreateClient(BaseModel):
    title: str


class TaskTypeCreateDB(BaseModel):
    title: str
    user_id: int


class TaskTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str

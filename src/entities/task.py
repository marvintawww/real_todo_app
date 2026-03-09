from pydantic import BaseModel, ConfigDict
from datetime import datetime, date


class TaskCreateClient(BaseModel):
    title: str
    description: str | None = None
    task_date: datetime | None = None


class TaskCreateDB(BaseModel):
    title: str
    description: str | None = None
    task_date: date | None = None
    user_id: int
    type_id: int


class TaskInfoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    task_date: date | None = None


class TaskStatusUpdate(BaseModel):
    completed: bool | None = None


class TaskTypeShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime
    completed_at: datetime | None = None
    task_date: datetime
    type: TaskTypeShort

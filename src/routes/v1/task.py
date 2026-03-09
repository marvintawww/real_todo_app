from src.dependencies.authenticate import get_current_user
from src.dependencies.task import get_task_service
from src.entities.task import (
    TaskCreateClient,
    TaskResponse,
    TaskInfoUpdate,
    TaskStatusUpdate,
)
from src.services.task import TaskService

from fastapi import Depends, status, APIRouter, Query
from datetime import date


router = APIRouter()


@router.post(
    "/tasks/create/{type_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Создать задачу",
)
async def create_task(
    data: TaskCreateClient,
    type_id: int,
    current_user: dict = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    user_id = int(current_user.get("sub"))
    return await task_service.create_task(user_id, type_id, data)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить задачу",
)
async def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    user_id = int(current_user.get("sub"))
    return await task_service.get_task(user_id, task_id)


@router.get(
    "/tasks",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить все задачи",
)
async def get_all_tasks(
    current_user: dict = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
    skip: int = 0,
    limit: int = 10,
    search_query: str | None = None,
    completed: bool | None = None,
    task_date: date | None = None,
    task_type: list[str] | None = Query(default=None),
) -> list[TaskResponse]:
    user_id = int(current_user.get("sub"))
    return await task_service.get_all_tasks(
        user_id=user_id,
        skip=skip,
        limit=limit,
        search_query=search_query,
        completed=completed,
        task_date=task_date,
        task_type=task_type,
    )


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновление задачи",
)
async def task_update(
    task_id: int,
    data: TaskInfoUpdate,
    current_user: dict = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    user_id = int(current_user.get("sub"))
    return await task_service.update_task(user_id, task_id, data)


@router.delete(
    "/tasks/{task_id}", status_code=status.HTTP_200_OK, summary="Удаление задачи"
)
async def task_delete(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> dict:
    user_id = int(current_user.get("sub"))
    return await task_service.delete_task(user_id, task_id)


@router.patch(
    "/tasks/{task_id}/status",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновление статуса задачи",
)
async def task_status_update(
    task_id: int,
    data: TaskStatusUpdate,
    current_user: dict = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    user_id = int(current_user.get("sub"))
    return await task_service.task_status_update(user_id, task_id, data)

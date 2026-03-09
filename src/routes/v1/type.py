from src.dependencies.type import get_type_service
from src.dependencies.authenticate import get_current_user
from src.entities.type import TaskTypeCreateClient, TaskTypeResponse
from src.services.type import TypeService

from fastapi import APIRouter, Depends, status

router = APIRouter()


@router.post(
    "/type",
    response_model=TaskTypeResponse,
    status_code=status.HTTP_200_OK,
    summary="Создание типа задачи",
)
async def create_type(
    data: TaskTypeCreateClient,
    current_user: dict = Depends(get_current_user),
    type_service: TypeService = Depends(get_type_service),
) -> TaskTypeResponse:
    user_id = int(current_user.get("sub"))
    return await type_service.create_type(user_id, data)


@router.get(
    "/type/{type_id}",
    response_model=TaskTypeResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить тип задачи",
)
async def get_type(
    type_id: int,
    current_user: dict = Depends(get_current_user),
    type_service: TypeService = Depends(get_type_service),
) -> TaskTypeResponse:
    user_id = int(current_user.get("sub"))
    return await type_service.get_task_type(user_id, type_id)


@router.get(
    "/types",
    response_model=list[TaskTypeResponse],
    status_code=status.HTTP_200_OK,
    summary="Все типы",
)
async def get_all_types(
    current_user: dict = Depends(get_current_user),
    type_service: TypeService = Depends(get_type_service),
    skip: int = 0,
    limit: int = 10,
) -> list[TaskTypeResponse]:
    user_id = int(current_user.get("sub"))
    return await type_service.get_all_types(user_id=user_id, skip=skip, limit=limit)

from src.entities.type import TaskTypeCreateClient, TaskTypeCreateDB
from src.models.type import TaskType
from src.exceptions.exceptions import ItemAlreadyExist, ItemNotExist


class TypeService:
    def __init__(self, query, command):
        self._query = query
        self._command = command

    async def _check_type_not_exist(self, user_id: int, title: str):
        task_type = await self._query.get_by_user_and_title(user_id, title)
        if task_type:
            raise ItemAlreadyExist

    async def get_task_type(self, user_id: int, type_id: int) -> TaskType:
        task_type = await self._query.get_by_user_and_id(user_id, type_id)
        if not task_type:
            raise ItemNotExist
        return task_type

    async def create_type(self, user_id: int, data: TaskTypeCreateClient) -> TaskType:
        await self._check_type_not_exist(user_id, data.title)
        task_type_data = TaskTypeCreateDB(title=data.title, user_id=user_id)
        return await self._command.create(task_type_data)

    async def get_all_types(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> list[TaskType]:
        return await self._query.get_all_types(user_id=user_id, skip=skip, limit=limit)

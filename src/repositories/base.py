from typing import TypeVar, Generic, Type
from abc import ABC, abstractmethod

from sqlalchemy import select

T = TypeVar("T")
C = TypeVar("C")
U = TypeVar("U")


class AbstractQueryRepository(ABC, Generic[T]):
    def __init__(self, session, model: Type[T]):
        self._session = session
        self._model = model

    @abstractmethod
    async def get_by_id(self, id: int) -> T | None:
        pass


class AbstractCommandRepository(ABC, Generic[T, C]):
    def __init__(self, session, model: Type[T]):
        self._session = session
        self._model = model

    @abstractmethod
    async def create(self, data: C) -> T:
        pass


class BaseQueryRepository(AbstractQueryRepository[T]):
    def __init__(self, session, model):
        super().__init__(session, model)

    async def get_by_id(self, id) -> T | None:
        stmt = select(self._model).where(self._model.id == id)
        obj = await self._session.execute(stmt)
        return obj.scalar_one_or_none()


class BaseCommandRepository(AbstractCommandRepository[T, C]):
    def __init__(self, session, model):
        super().__init__(session, model)

    async def _commit(self, obj: T):
        await self._session.commit()
        await self._session.refresh(obj)

    async def create(self, data: C) -> T:
        try:
            obj = self._model(**data.model_dump())
            self._session.add(obj)
            await self._commit(obj)
            return obj
        except Exception:
            await self._session.rollback()
            raise

    async def update(self, obj: T, data: U) -> T:
        try:
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(obj, key, value)
            await self._commit(obj)
            return obj
        except Exception:
            await self._session.rollback()
            raise

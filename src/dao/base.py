from typing import Generic, Sequence, Type, TypeVar

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.base import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model = Type[T]

    def __init_subclass__(cls, **kwargs):
        if not hasattr(cls, "model"):
            raise NotImplementedError(f"{cls.__name__} must define a 'model' class attribute")

    @classmethod
    async def get_by_id(cls, session: AsyncSession, obj_id: int) -> T | None:
        try:
            return await session.get(cls.model, obj_id)
        except SQLAlchemyError as e:
            logger.error(f"❌ Error getting {cls.model.__name__} with ID: {obj_id}: {e}")
            raise

    @classmethod
    async def find_one_by_kwargs(cls, session: AsyncSession, **kwargs) -> T | None:
        try:
            stmt = select(cls.model).filter_by(**kwargs)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error getting {cls.model.__name__} with {kwargs}: {e}")
            raise

    @classmethod
    async def find_all_by_kwargs(cls, session: AsyncSession, **kwargs) -> Sequence[T]:
        try:
            stmt = select(cls.model).filter_by(**kwargs)
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error getting classes {cls.model.__name__} with {kwargs}: {e}")
            raise

    @classmethod
    async def add(cls, session: AsyncSession, data: dict | BaseModel) -> T:
        data_dict = data.model_dump(exclude_unset=True) if isinstance(data, BaseModel) else data
        instance = cls.model(**data_dict)
        session.add(instance)
        try:
            await session.flush()
            logger.info(f"{cls.model.__name__} добавлена: {data_dict}")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"❌ Error adding {cls.model.__name__} to database: {e}")
            raise
        return instance

    @classmethod
    async def update_by_id(cls, session: AsyncSession, obj_id: int, data: dict | BaseModel) -> None:
        data_dict = data.model_dump(exclude_unset=True) if isinstance(data, BaseModel) else data
        try:
            obj = await session.get(cls.model, obj_id)
            if obj:
                for key, value in data_dict.items():
                    setattr(obj, key, value)
                await session.flush()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error updating{cls.model.__name__} with ID {obj_id}: {e}")
            raise

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, obj_id: int) -> None:
        try:
            obj = await session.get(cls.model, obj_id)
            if obj:
                await session.delete(obj)
                await session.flush()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error deleting {cls.model.__name__} with ID {obj_id}: {e}")
            raise

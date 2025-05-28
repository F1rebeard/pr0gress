from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import BaseDAO
from src.database.models.users import User


class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_by_telegram_id(cls, session: AsyncSession, telegram_id: int) -> User | None:
        stmt = select(cls.model).where(cls.model.telegram_id == telegram_id)
        try:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(
                f"❌ Error getting {cls.model.__name__} with telegram_id: {telegram_id}: {e}"
            )
            raise

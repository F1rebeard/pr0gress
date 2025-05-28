from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import BaseDAO
from src.database.models import Subscription


class SubscriptionDAO(BaseDAO[Subscription]):
    model = Subscription

    @classmethod
    async def get_by_user_id(cls, session: AsyncSession, user_id: int) -> Subscription | None:
        stmt = select(cls.model).where(cls.model.user_id == user_id)
        try:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(
                f"❌ Error getting {cls.model.__name__} with telegram_id: {user_id}: {e}"
            )
            raise

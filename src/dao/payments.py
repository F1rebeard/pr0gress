from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import BaseDAO
from src.database.models import Payment, Subscription


class PaymentDAO(BaseDAO[Payment]):
    model = Payment

    @classmethod
    async def find_latest_successful_payment(cls, session: AsyncSession, user_id: int) -> Payment | None:
        stmt = (
            select(cls.model)
            .join(Subscription, Subscription.user_id == user_id)
            .where(
                cls.model.status == "Выполнен",
                cls.model.sub_id == Subscription.user_id
            )
            .order_by(cls.model.payment_date.desc())
            .limit(1)
        )
        try:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"❌ Failed to find a succesfull payment for user {user_id}: {e}")
            raise

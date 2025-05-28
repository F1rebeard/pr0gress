from collections.abc import Sequence

from loguru import logger
from sqlalchemy import asc, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import BaseDAO
from src.database.models import FreeTrial, TrialWorkout


class FreeTrialDAO(BaseDAO[FreeTrial]):
    model = FreeTrial


class TrialWorkoutDAO(BaseDAO[TrialWorkout]):
    model = TrialWorkout

    @classmethod
    async def get_ordered_workouts(cls, session: AsyncSession) -> Sequence[TrialWorkout]:
        try:
            stmt = select(cls.model).order_by(asc(cls.model.workout_id))
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error getting classes {cls.model.__name__}: {e}")
            raise

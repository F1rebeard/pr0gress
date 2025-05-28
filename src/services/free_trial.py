from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.free_trial import FreeTrialDAO, TrialWorkoutDAO
from src.database.models import FreeTrial


class FreeTrialService:
    def __init__(self, session: AsyncSession, expiration_days: int = 10):
        self.session = session
        self.expiration_days = expiration_days

    async def get_or_create_trial_for_user(self, telegram_id: int) -> FreeTrial:
        """
        Creates a new trial for the user if it doesn't exist already.
        """
        trial = await FreeTrialDAO.get_by_id(self.session, telegram_id)
        if trial:
            return trial

        trial = await FreeTrialDAO.add(self.session, {"telegram_id": telegram_id})
        return trial

    async def is_trial_active(self, telegram_id: int) -> bool:
        """
        Determines if a trial period is currently active for the given user by checking
        the trial start date and the expiration period.
        """
        trial = await FreeTrialDAO.get_by_id(self.session, telegram_id)
        if not trial:
            return False
        if (date.today() - trial.start_date).days > self.expiration_days:
            return False
        return True

    async def get_trial_workouts(self):
        """
        Get all trial workouts from the database.
        """
        return await TrialWorkoutDAO.get_ordered_workouts(self.session)

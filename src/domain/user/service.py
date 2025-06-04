from src.dao import FreeTrialDAO, SubscriptionDAO, UserDAO
from src.domain.user.models import TrialStatus, UserStatus
from src.services.free_trial import FreeTrialService


class UserStatusService:
    def __init__(self, session):
        self.session = session

    async def get_user_status(self, telegram_id: int):
        user = await UserDAO.get_by_id(self.session, telegram_id)
        subscription = await SubscriptionDAO.get_by_user_id(self.session, telegram_id)

        # Test week trial check
        trial = await FreeTrialDAO.get_by_id(self.session, telegram_id)
        trial_service = FreeTrialService(self.session)
        is_trial_active = await trial_service.is_trial_active(telegram_id)

        if not trial:
            trial_status = TrialStatus.NOT_USED
        elif is_trial_active:
            trial_status = TrialStatus.ACTIVE
        else:
            trial_status = TrialStatus.EXPIRED

        return UserStatus(
            user=user,
            subscription=subscription,
            trial_status=trial_status,
        )

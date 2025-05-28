from src.dao import SubscriptionDAO, UserDAO
from src.domain.user.context import UserContext


class UserContextService:
    def __init__(self, session):
        self.session = session

    async def get_user_context(self, telegram_id: int):
        user = await UserDAO.get_by_id(self.session, telegram_id)
        subscription = await SubscriptionDAO.get_by_user_id(self.session, telegram_id)
        return UserContext(telegram_id, user, subscription)

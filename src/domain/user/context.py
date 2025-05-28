from src.database.models import Subscription, User
from src.database.models.subscriptions import SubscriptionStatus


class UserContext:
    def __init__(self, telegram_id: int, user: User | None, subscription: Subscription | None):
        self.telegram_id = telegram_id
        self.user = user
        self.subscription = subscription

    @property
    def is_new_user(self) -> bool:
        return not self.subscription

    @property
    def needs_registration(self) -> bool:
        return self.subscription and self.subscription.status == SubscriptionStatus.UNREGISTERED

    @property
    def is_active(self) -> bool:
        return self.subscription and self.subscription.status == SubscriptionStatus.ACTIVE

    @property
    def is_frozen(self) -> bool:
        return self.subscription and self.subscription.status == SubscriptionStatus.FROZEN

    @property
    def is_expired(self) -> bool:
        return self.subscription and self.subscription.status == SubscriptionStatus.EXPIRED

    @property
    def is_trial(self):
        pass

    @property
    def is_banned(self) -> bool:
        return self.subscription and self.subscription.status == SubscriptionStatus.BANNED

from src.database.models import Subscription, TrialStatus, User
from src.database.models.subscriptions import SubscriptionStatus


class UserStatus:
    def __init__(
        self,
        user: User | None,
        subscription: Subscription | None,
        trial_status: TrialStatus= TrialStatus.NOT_USED,
    ):
        self.user = user
        self.subscription = subscription
        self.trial_status = trial_status

    @property
    def is_new_user(self) -> bool:
        return not self.subscription and self.trial_status == TrialStatus.NOT_USED

    @property
    def is_trial(self) -> bool:
        return not self.subscription and self.trial_status == TrialStatus.ACTIVE

    @property
    def had_trial_but_not_active(self) -> bool:
        return not self.subscription and self.trial_status == TrialStatus.EXPIRED

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
    def is_banned(self) -> bool:
        return self.subscription and self.subscription.status == SubscriptionStatus.BANNED

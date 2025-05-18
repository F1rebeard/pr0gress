import enum
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base


class SubscriptionType(str, enum.Enum):
    STANDARD = "Базовая"
    WITH_CURATOR = "С куратором"
    START_FULL = "Полный Старт"
    START_MONTH = "Месяц Старт"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "Активна"
    FROZEN = "Заморожена"
    EXPIRED = "Истекла"
    UNREGISTERED = "Оплата без регистрации"


class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    subscription_type: Mapped[SubscriptionType] = mapped_column(
        Enum(SubscriptionType, name="sub_type_enum"), nullable=False
    )
    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus, name="sub_status_enum"), nullable=False)
    registered_date: Mapped[Date] = mapped_column(Date, server_default=func.now(), nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    start_program_begin_date: Mapped[Date | None] = mapped_column(Date, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="subscription",
        uselist=False,
        lazy="selectin",
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="subscription",
        cascade="all, delete, delete-orphan",
    )

import enum
import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base
from src.database.models.subscriptions import SubscriptionType


class PaymentStatus(str, enum.Enum):
    PENDING = "Обработка"
    COMPLETED = "Выполнен"
    FAILED = "Ошибка"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sub_id: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.user_id", ondelete="RESTRICT"), nullable=False
    )
    sub_type: Mapped[SubscriptionType] = mapped_column(
        Enum(SubscriptionType, name="sub_type_enum", create_type=False), nullable=False
    )
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), nullable=False)
    payment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    # Relation
    subscription: Mapped["Subscription"] = relationship(
        "Subscription",
        back_populates="payments",
    )

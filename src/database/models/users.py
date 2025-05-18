import enum

from sqlalchemy import BigInteger, Enum, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models import Base


class UserLevel(str, enum.Enum):
    FIRST = "Первый"
    SECOND = "Второй"
    MINKAIFA = "Минкайфа"
    COMPETITION = "Соревнования"
    START = "Старт"


class UserRole(str, enum.Enum):
    ADMIN = "Админ"
    CURATOR = "Куратор"
    USER = "Пользователь"


class Gender(str, enum.Enum):
    MALE = "Парень ♂️"
    FEMALE = "Девушка ♀️"


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    username: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    e_mail: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    gender: Mapped[Gender | None] = mapped_column(
        Enum(Gender, name="gender_enum"), nullable=True)
    level: Mapped[UserLevel | None] = mapped_column(
        Enum(UserLevel, name="user_level_enum"), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(
        UserRole, name="user_role_enum"), default=UserRole.USER)

    # Relations
    subscription: Mapped["Subscription"] = relationship(
        "Subscription",
        back_populates="user",
        lazy="selectin",
    )
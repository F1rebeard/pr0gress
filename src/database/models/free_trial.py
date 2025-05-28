from datetime import date

from sqlalchemy import BigInteger, Date, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import Base


class FreeTrial(Base):
    __tablename__ = "free_trials"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False ,default=date.today)


class TrialWorkout(Base):
    __tablename__ = "trial_workouts"

    workout_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    position: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

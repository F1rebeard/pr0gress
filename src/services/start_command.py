from aiogram.types import InlineKeyboardMarkup
from loguru import logger

from src.bot.keyboards.subscription import (
    renew_or_change_subscription_kb,
    subs_kb,
    subs_or_trial_kb,
    to_registration_btn,
    unfreeze_subscription_kb,
)
from src.bot.keyboards.utils import create_inline_keyboard
from src.domain.user.context import UserContext
from src.services.free_trial import FreeTrialService
from src.services.main_menu import MainMenuService


class StartCommandService:
    def __init__(self, session):
        self.session = session

    async def get_start_message(self, ctx: UserContext) -> tuple[str, InlineKeyboardMarkup | None]:
        if ctx.is_new_user:
            return (
                '🔥 Привет!\nДобро пожаловать в <b>Прогресс</b>!\n\n'
                'Можешь взять пробную неделю и попробовать наши тренировки, '
                'а можешь сразу выбрать подходящую подписку‍.',
                subs_or_trial_kb
            )
        if ctx.needs_registration:
            return (
                '🏋️‍♂️ Почти готово!\nПодписка <b>оплачена</b>.\n'
                '📝 Остался последний шаг – заполни данные, и начни тренировки!',
                to_registration_btn
            )
        if ctx.is_frozen:
            return (
                '❄️ <b>Подписка заморожена</b>\n\n'
                'Мы скучаем по твоим рекордам, а штанга застоялась…\n'
                '👉 <b>Разморозь подписку</b> и возвращайся в игру! 🏋️‍♀️',
                unfreeze_subscription_kb
            )
        if ctx.is_expired:
            return (
                'Твоя подписка <b>закончилась 😢</b>.\n'
                '🔥 Но ты можешь вернуться в Прогресс прямо сейчас!\n'
                '📌 Обнови подписку и продолжай тренироваться с нами!\n',
                renew_or_change_subscription_kb
            )
        if ctx.is_active:
            return await MainMenuService(self.session).get_main_menu_text_and_markup(ctx.telegram_id)

        logger.error("❗ Unknown user state encountered")
        return "❗Что-то пошло не так. Попробуйте позже.", None

    async def try_free_trial(self, telegram_id: int) -> tuple[str, InlineKeyboardMarkup]:
        trial_service = FreeTrialService(self.session)
        await trial_service.get_or_create_trial_for_user(telegram_id)
        is_active = await trial_service.is_trial_active(telegram_id)
        if not is_active:
            return (
                "Пробная неделя истекла 😢. Оформи подписку, и присоединяйся к нам 🏋️",
                subs_kb
            )

        trial_workouts = await trial_service.get_trial_workouts()
        markup_kb = create_inline_keyboard(
            [
                (f"Тренировка №{workout.position}", f"{workout.workout_id}")
                for workout in trial_workouts
            ]
        )
        return (
            "ТУТ БУДЕТ ИНСТРУКЦИЯ К ПРОБНЫМ ТРЕНИРОВКАМ И ОПИСАНИЕ",
            markup_kb
        )

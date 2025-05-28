from datetime import date

from aiogram.types import InlineKeyboardMarkup

from src.bot.keyboards.main_menu import get_main_menu_keyboard
from src.dao import SubscriptionDAO, UserDAO

BEGIN_NOTIFICATIONS_DAYS = 3


class MainMenuService:
    def __init__(self, session):
        self.session = session

    async def get_main_menu_text_and_markup(self, telegram_id: int) -> tuple[str, InlineKeyboardMarkup]:
        user = await UserDAO.get_by_id(self.session, telegram_id)
        subscription = await SubscriptionDAO.get_by_id(self.session, telegram_id)
        days_left = (subscription.end_date - date.today()).days

        text = (
            "📱 <b>Главное меню</b>\n\n"
            f"🏋️‍♂️ <b>Уровень:</b> {user.level or 'Не выбран'}\n"
            f"📅 <b>Подписка до:</b> {subscription.end_date.strftime('%d.%m.%Y')}\n"
        )

        if days_left <= BEGIN_NOTIFICATIONS_DAYS:
            text += f"🔔⚠️ <b>Осталось дней:</b> {days_left}"
        else:
            text += f"⏳✅️ <b>Осталось дней:</b> {days_left}"

        return text, get_main_menu_keyboard()

from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.database import db
from src.services.start_command import StartCommandService

free_trial_router = Router()


@free_trial_router.callback_query(F.data == "trial_week")
async def choose_trial_week(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    await callback.message.answer("Попка")
    async with db.session() as session:
        start_service = StartCommandService(session)
        text, markup_kb = await start_service.try_free_trial(telegram_id)
        await callback.message.edit_text(text, reply_markup=markup_kb)

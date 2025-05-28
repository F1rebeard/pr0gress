from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

from src.database.connection import db
from src.domain.user.service import UserContextService
from src.services.start_command import StartCommandService

starting_router = Router()


@starting_router.message(CommandStart())
async def start_the_bot(message: Message):
    telegram_id = message.from_user.id

    async with db.session() as session:
        try:
            context_service = UserContextService(session)
            context = await context_service.get_user_context(telegram_id)
            start_service = StartCommandService(session)
            text, markup = await start_service.get_start_message(context)
            await message.answer(text, reply_markup=markup)
        except Exception as e:
            logger.exception(f"Failed to process /start command for user {telegram_id}: {e}")
            await message.answer("❗Что-то пошло не так. Напиши нам, поможем!")

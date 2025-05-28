import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from src.bot.handlers.free_trial import free_trial_router
from src.bot.handlers.starting import starting_router
from src.config import settings
from src.database import db
from src.logger import setup_logger

bot_properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
)
bot = Bot(
    token=settings.BOT_TOKEN,
    default=bot_properties
)
dp = Dispatcher()


@asynccontextmanager
async def app_lifecycle():
    setup_logger()
    logger.info("🚀 Starting...")
    await db.connect()
    try:
        yield {"bot": bot}
    finally:
        await db.disconnect()
        await bot.session.close()
        logger.info("🛑 Shutting down...")


async def main():
    async with app_lifecycle() as app:
        bot = app["bot"]
        dp.include_router(starting_router)
        dp.include_router(free_trial_router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

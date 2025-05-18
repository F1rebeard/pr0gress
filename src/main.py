import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from loguru import logger

from src.logger import setup_logger
from src.config import settings
from src.database import db


bot_properties = DefaultBotProperties(
    parse_mode=ParseMode.MARKDOWN_V2,
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
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
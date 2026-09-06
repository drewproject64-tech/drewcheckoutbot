from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.bot.handlers.admin_payments import router as admin_router
from app.bot.handlers.menu import router as menu_router
from app.bot.handlers.payments import router as payments_router
from app.bot.handlers.start import router as start_router
from app.bot.language import router as language_router
from app.bot.middleware import DbSessionMiddleware
from app.config import load_settings
from app.database.database import Database
from app.services.expiration_worker import process_subscriptions

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    settings = load_settings()
    logging.getLogger().setLevel(settings.log_level)

    db = Database(settings)
    await db.init()
    logger.info("Database initialized.")

    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    db_middleware = DbSessionMiddleware(db, settings)
    dp.message.middleware(db_middleware)
    dp.callback_query.middleware(db_middleware)

    dp.include_router(language_router)
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(payments_router)
    dp.include_router(admin_router)

    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(process_subscriptions, "interval", minutes=10, args=[bot, db, settings], max_instances=1, coalesce=True)
    scheduler.start()
    logger.info("Expiration worker started.")

    try:
        logger.info("Drew FX Payment Bot starting...")
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()
        await db.close()
        logger.info("Drew FX Payment Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.api.server import create_app, start_server
from bot.config import config
from bot.db import close_db, init_db
from bot.handlers import register_handlers
from bot.services import achievement as achievement_service
from bot.services import entity_type as et_service

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    await init_db()
    logger.info("supabase client initialized")

    await et_service.load_entity_types()
    logger.info("loaded %d entity types", len(et_service.get_all()))

    await achievement_service.load_achievements()
    logger.info("loaded %d achievements", len(achievement_service.get_all()))

    register_handlers(dp)

    app = create_app(bot)
    server_task = asyncio.create_task(start_server(app, config.api_host, config.api_port))
    logger.info("api server starting on %s:%d", config.api_host, config.api_port)

    try:
        await dp.start_polling(bot)
    finally:
        server_task.cancel()
        await close_db()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

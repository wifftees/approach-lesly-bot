from aiogram import Dispatcher

from bot.handlers.add_entry import router as add_entry_router
from bot.handlers.start import router as start_router
from bot.handlers.stats import router as stats_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(stats_router)
    dp.include_router(add_entry_router)

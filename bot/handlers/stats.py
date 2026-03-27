from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from bot.config import config
from bot.services import activity as activity_service

router = Router()


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    await activity_service.log_activity(message.from_user.id, "command", {"command": "/stats"})

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Статистика 📊", web_app=WebAppInfo(url=config.webapp_url))]
    ])
    await message.answer("Открой статистику:", reply_markup=keyboard)

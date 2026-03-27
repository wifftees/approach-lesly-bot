from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.keyboards import main_keyboard
from bot.services import entity_type as et_service
from bot.services import user as user_service
from bot.services import activity as activity_service

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user = message.from_user
    await user_service.upsert_user(user.id, user.username, user.first_name, user.last_name)
    await activity_service.log_activity(user.id, "command", {"command": "/start"})

    entity_types = et_service.get_all()
    commands_text = "\n".join(
        f"  {et.command} — {et.display_name} (+{et.points} очков)"
        for et in entity_types
    )

    text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Добро пожаловать в бот для учёта подходов. Фиксируй свои результаты, соревнуйся с друзьями и собирай ачивки!\n\n"
        "📝 Как это работает:\n"
        f"{commands_text}\n\n"
        "Красивая девочка — это 7+. За неё нужно указать контакт и получишь больше очков.\n\n"
        "🏆 Лидерборд\n"
        "Все участники ранжируются по очкам. Видно кто на каком месте и с каким отрывом. Соревнование в реальном времени — каждый новый подход сразу меняет таблицу.\n\n"
        "🔍 Прозрачность и проверка на читерство\n"
        "Каждая запись публична. В специальной вкладке можно посмотреть историю любого участника — кого и когда он добавил. Если кто-то накручивает очки — это сразу видно.\n\n"
        "🎖 Ачивки\n"
        "За каждую категорию можно получить достижения по мере роста счётчика. Чем больше подходов — тем круче звание. Ачивки отображаются в профиле.\n\n"
        "📊 /stats — открыть статистику, лидерборд и ачивки\n"
        "❓ /help — список команд\n\n"
        "Жми кнопки внизу и поехали! 🚀"
    )
    await message.answer(text, reply_markup=main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await activity_service.log_activity(message.from_user.id, "command", {"command": "/help"})

    entity_types = et_service.get_all()
    lines = [f"{et.command} — {et.display_name} (+{et.points} очков)" for et in entity_types]
    lines.append("/stats — Статистика и лидерборд 📊")
    lines.append("/help — Эта справка ❓")

    text = "Доступные команды:\n\n" + "\n".join(lines)
    await message.answer(text, reply_markup=main_keyboard())

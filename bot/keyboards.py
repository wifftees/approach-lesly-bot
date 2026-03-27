from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.services import entity_type as et_service


def main_keyboard() -> ReplyKeyboardMarkup:
    entity_types = et_service.get_all()
    buttons = [[KeyboardButton(text=et.command)] for et in entity_types]
    buttons.append([KeyboardButton(text="/stats"), KeyboardButton(text="/help")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def contact_keyboard(contact_required: bool) -> InlineKeyboardMarkup:
    buttons = []
    if not contact_required:
        buttons.append(InlineKeyboardButton(text="Пропустить", callback_data="skip_contact"))
    buttons.append(InlineKeyboardButton(text="Отмена", callback_data="cancel_entry"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

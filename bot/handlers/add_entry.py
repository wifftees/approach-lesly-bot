import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.keyboards import contact_keyboard, main_keyboard
from bot.services import achievement as achievement_service
from bot.services import activity as activity_service
from bot.services import entity_type as et_service
from bot.services import entry as entry_service
from bot.services import user as user_service

router = Router()


class AddEntryStates(StatesGroup):
    waiting_contact = State()


@router.message(F.text.startswith("/add_"))
async def cmd_add_entry(message: Message, state: FSMContext) -> None:
    command = message.text.split()[0]
    entity_type = et_service.get_by_command(command)
    if not entity_type:
        return

    user = message.from_user
    await user_service.upsert_user(user.id, user.username, user.first_name, user.last_name)
    await activity_service.log_activity(user.id, "command", {"command": command})

    await state.set_state(AddEntryStates.waiting_contact)
    await state.update_data(entity_type_id=entity_type.id, entity_type_slug=entity_type.slug)

    prompt = f"Введи @username контакта для «{entity_type.display_name}»:"
    await message.answer(prompt, reply_markup=contact_keyboard(entity_type.contact_required))


@router.callback_query(F.data == "skip_contact")
async def on_skip_contact(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    if not data:
        await callback.answer("Нет активной операции")
        return

    entity_type_id = data["entity_type_id"]
    entity_type_slug = data["entity_type_slug"]
    user_id = callback.from_user.id

    entry_id = await entry_service.create_entry(user_id, entity_type_id, None)
    await activity_service.log_activity(user_id, "add_entry", {"entity_type_slug": entity_type_slug, "entry_id": entry_id})
    await state.clear()

    et = et_service.get_by_slug(entity_type_slug)
    congrats = random.choice(et.congratulation_texts).replace("{points}", str(et.points))
    await callback.message.edit_text(congrats)

    count = await entry_service.get_entries_count(user_id, entity_type_id)
    new_achievements = await achievement_service.check_and_grant(user_id, entity_type_id, count)
    for ach in new_achievements:
        await callback.message.answer(f"🏆 Ачивка разблокирована: {ach.emoji} {ach.name}!")

    await callback.message.answer("Записано!", reply_markup=main_keyboard())
    await callback.answer()


@router.callback_query(F.data == "cancel_entry")
async def on_cancel_entry(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("Отменено ❌")
    await callback.answer()


@router.message(AddEntryStates.waiting_contact)
async def on_contact_input(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if not data:
        return

    contact = message.text.strip().lstrip("@")
    entity_type_id = data["entity_type_id"]
    entity_type_slug = data["entity_type_slug"]
    user_id = message.from_user.id

    entry_id = await entry_service.create_entry(user_id, entity_type_id, contact)
    await activity_service.log_activity(user_id, "add_entry", {"entity_type_slug": entity_type_slug, "entry_id": entry_id})
    await state.clear()

    et = et_service.get_by_slug(entity_type_slug)
    congrats = random.choice(et.congratulation_texts).replace("{points}", str(et.points))
    await message.answer(congrats)

    count = await entry_service.get_entries_count(user_id, entity_type_id)
    new_achievements = await achievement_service.check_and_grant(user_id, entity_type_id, count)
    for ach in new_achievements:
        await message.answer(f"🏆 Ачивка разблокирована: {ach.emoji} {ach.name}!")

    await message.answer("Записано!", reply_markup=main_keyboard())

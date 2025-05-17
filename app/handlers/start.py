from aiogram import Router
from aiogram.types import Message

# from app.service.user_service import get_or_create_user_role


router = Router()

@router.message(lambda msg: msg.text == "/start")
async def start_handler(message: Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    # Получаем роль или создаем запись
    # role = await get_or_create_user_role(user_id, full_name)

    await message.answer(
        f"👋 Привет, {full_name}!\n"
        # f"Ты зарегистрирован как <b>{role}</b>.\n\n"
        f"Введи /help для списка команд.",
        parse_mode="HTML"
    )

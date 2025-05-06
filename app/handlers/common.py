# app/handlers/common.py

from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda msg: msg.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Привет! Я бот картинной галереи. Введи /help для списка команд.")

@router.message(lambda msg: msg.text == "/help")
async def help_handler(message: Message):
    await message.answer(
        "📚 Доступные команды:\n"
        "/catalog — каталог картин\n"
        "/artists — список художников\n"
        "/artists_<id> - информация о художнике\n"
        "/art_<id> — информация о картине\n"
        "/qr_<id> — QR-код картины"
    )

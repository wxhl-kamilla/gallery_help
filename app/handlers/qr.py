# app/handlers/qr.py
import io

import qrcode
from aiogram import Router
from aiogram.types import Message, InputFile, BufferedInputFile
from app.database import get_session
from app.models.painting import Painting
from app.service import get_all_paintings, get_all_artists

router = Router()

@router.message(lambda msg: msg.text.startswith("/qr_"))
async def qr_handler(message: Message):
    # Получаем ID картины из сообщения
    try:
        painting_id = int(message.text.split('_')[1])
    except (IndexError, ValueError):
        await message.answer("🚨 Неверный формат команды. Используйте: /qr_<id картины>")
        return

    async for session in get_session():
        paintings = await get_all_paintings(session)
        artists = await get_all_artists(session)

    for p in paintings:
        if p.id == painting_id:
            painting = p

    for a in artists:
        if a.id == painting_id:
            artist = a

    if not painting:
        await message.answer(f"🖼️ Картина с ID {painting_id} не найдена.")
        return

    # Генерация QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(f"Картина: {painting.title}\nАвтор: {a.name}")
    qr.make(fit=True)
    # Создаем изображение в памяти
    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()

    # Создаем BufferedInputFile
    photo = BufferedInputFile(img_bytes, filename=f"qr_{painting_id}.png")

    await message.answer_photo(
        photo,
        caption=f"QR-код для картины: {painting.title}"
    )
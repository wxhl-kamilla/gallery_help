# app/handlers/artist.py
from http.client import responses

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.artist import Artist
from app.service.artist_service import get_all_artists, get_artist_by_id

router = Router()

@router.message(Command("artists"))
async def artists_handler(message: Message):
    async for session in get_session():  # Используем get_db как асинхронный генератор
        artists = await get_all_artists(session)

        if not artists:
            await message.answer("🧑‍🎨 Художники пока не добавлены.")
            return

        response = "🧑‍🎨 Список художников:\n\n"
        for artist in artists:
            response += f"/artist_{artist.id} - {artist.name}\n"

        await message.answer(response)


@router.message(lambda msg: msg.text and msg.text.startswith('/artist_'))
async def artist_detail_handler(message: Message):
    try:
        artist_id = int(message.text.split('_')[1])
    except (IndexError, ValueError):
        await message.answer("🚨 Неверный формат команды. Используйте /artist_1")
        return

    async for session in get_session():
        artists = await get_all_artists(session)
        if not artists:
            await message.answer("🚨 Художник не найден")
            return

    for a in artists:
        if a.id == artist_id:
            response = (
                f'{a.name}\n'
                f'{a.birth_year}\n'
                f'{a.death_year}\n'
                f'{a.bio}'
            )

    await message.answer(response)
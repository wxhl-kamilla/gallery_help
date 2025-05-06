# app/services/painting_service.py
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.painting import Painting
from app.models.artist import Artist

async def get_all_paintings(session: AsyncSession):
    result = await session.execute(select(Painting).join(Artist))
    paintings = result.scalars().all()
    return paintings


async def get_painting_by_id(
        session: AsyncSession,
        painting_id: int,
        include_artist: bool = True
) -> Optional[Painting]:
    """
    Получает картину по ID из базы данных

    Параметры:
        session (AsyncSession): Асинхронная сессия SQLAlchemy
        painting_id (int): ID картины для поиска
        include_artist (bool): Загружать связанного художника (по умолчанию True)

    Возвращает:
        Optional[Painting]: Объект картины или None, если не найдена
    """
    try:
        # Создаем базовый запрос
        query = select(Painting).where(Painting.id == painting_id)

        # Если нужно загрузить информацию о художнике
        if include_artist:
            query = query.options(selectinload(Painting.artist))

        # Выполняем запрос
        result = await session.execute(query)

        # Получаем первый результат (или None)
        painting = result.scalars().first()

        return painting

    except Exception as e:
        # Логируем ошибку, если нужно
        # logger.error(f"Error fetching painting: {e}")
        return None
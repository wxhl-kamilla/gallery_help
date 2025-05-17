# app/service/artist_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.artist import Artist

async def get_all_artists(session: AsyncSession):
    result = await session.execute(select(Artist))
    return result.scalars().all()

async def get_artist_by_id(session: AsyncSession, artist_id: int) -> Artist | None:
    result = await session.execute(select(Artist).where(Artist.id == artist_id))
    return result.scalars().first()
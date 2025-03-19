from fastapi import FastAPI, HTTPException
from database import db_session
from models.artist import Artist
from services.artist_service import ArtistService

app = FastAPI()

artist_service = ArtistService()

@app.get("/artist/{artist_id}")
async def get_artist(artist_id: int):
    """
    Получить информацию о художнике по его ID.

    Параметры:
    - artist_id (int): ID художника

    Возвращает:
    - dict: Информация о художнике
    """
    artist = artist_service.get_artist_info(artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Художник не найден")
    return artist

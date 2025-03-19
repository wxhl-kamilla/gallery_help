from backend.database import db_session
from backend.models.artist import Artist
class ArtistService:
    """
    Класс для управления данными о художниках.

    Методы:
    - get_artist_info: Получает информацию о художнике по его ID
    """
    def get_artist_info(self, artist_id: int) -> dict:
        """
        Получает информацию о художнике по его ID.

        Параметры:
        - artist_id (int): ID художника

        Возвращает:
        - dict: Информация о художнике или None, если художник не найден
        """
        artist = db_session.query(Artist).filter(Artist.id == artist_id).first()
        if artist:
            return {"id": artist.id, "name": artist.name, "bio": artist.bio}
        return None


    def get_all_artists(self) -> list:
        """
        Получает список всех художников.

        Возвращает:
        - list: Список словарей с данными о каждом художнике
        """
        artists = db_session.query(Artist).all()
        return [{"id": artist.id, "name": artist.name, "bio": artist.bio} for artist in artists]
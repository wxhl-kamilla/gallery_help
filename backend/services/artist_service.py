from backend.models.db_session import create_session
from backend.models.artist import Artist
from typing import List, Optional

class ArtistService:
    @staticmethod
    def create_artist(name: str, **kwargs) -> Artist:
        """Создание нового художника"""
        session = create_session()
        try:
            artist = Artist(name=name, **kwargs)
            session.add(artist)
            session.commit()
            return artist
        finally:
            session.close()

    @staticmethod
    def get_all() -> List[Artist]:
        """Получение всех художников"""
        session = create_session()
        try:
            return session.query(Artist).all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(artist_id: int) -> Optional[Artist]:
        """Получение художника по ID"""
        session = create_session()
        try:
            return session.query(Artist).get(artist_id)
        finally:
            session.close()
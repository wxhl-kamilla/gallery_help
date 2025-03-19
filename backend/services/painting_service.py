from backend.database import db_session
from backend.models.painting import Painting


class PaintingService:
    """
    Сервис для работы с данными о картинах.

    Методы:
    - get_painting_info: Получает информацию о картине по её ID
    - get_all_paintings: Получает список всех картин
    """

    def get_painting_info(self, painting_id: int) -> dict:
        """
        Получает информацию о картине по её ID.

        Параметры:
        - painting_id (int): ID картины

        Возвращает:
        - dict: Информация о картине или None, если не найдена
        """
        painting = db_session.query(Painting).filter(Painting.id == painting_id).first()
        if painting:
            return {
                "id": painting.id,
                "title": painting.title,
                "artist_id": painting.artist_id,
                "description": painting.description
            }
        return None

    def get_all_paintings(self) -> list:
        """
        Получает список всех картин.

        Возвращает:
        - list: Список словарей с данными о каждой картине
        """
        paintings = db_session.query(Painting).all()
        return [
            {
                "id": painting.id,
                "title": painting.title,
                "artist_id": painting.artist_id,
                "description": painting.description
            }
            for painting in paintings
        ]

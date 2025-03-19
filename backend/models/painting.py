from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base

class Painting(Base):
    """
    Модель данных для хранения информации о картинах.

    Атрибуты:
    - id (int): Уникальный идентификатор картины
    - title (str): Название картины
    - artist_id (int): ID художника (внешний ключ)
    - description (str): Описание картины
    """
    __tablename__ = "paintings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    description = Column(String)

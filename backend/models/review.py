from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base

class Review(Base):
    """
    Модель данных для хранения отзывов о картинах и выставке.

    Атрибуты:
    - id (int): Уникальный идентификатор отзыва
    - painting_id (int): ID картины, о которой оставлен отзыв (внешний ключ)
    - content (str): Текст отзыва
    - rating (int): Оценка по шкале 1-5
    """
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    painting_id = Column(Integer, ForeignKey("paintings.id"), nullable=False)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

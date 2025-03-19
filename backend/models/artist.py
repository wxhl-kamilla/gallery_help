from backend.database import Base
from sqlalchemy import Column, Integer, String

class Artist(Base):
    """
    Класс, представляющий художника.

    Атрибуты:
    - id (int): Уникальный идентификатор художника
    - name (str): Имя художника
    - bio (str): Краткая биография
    """
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(String)

# app/models/painting.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import Base

class Painting(Base):
    __tablename__ = 'paintings'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)

    # Определяем отношения с художником
    artist = relationship("Artist", back_populates="paintings")
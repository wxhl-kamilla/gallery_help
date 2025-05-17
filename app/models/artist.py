# app/models/artist.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_year = Column(Integer)
    death_year = Column(Integer)
    bio = Column(String)

    # Определяем отношения с картиной
    paintings = relationship("Painting", back_populates="artist")
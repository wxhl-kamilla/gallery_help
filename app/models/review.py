# app/models/review.py

from sqlalchemy import Column, Integer, Text, ForeignKey
from app.models.base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    painting_id = Column(Integer, ForeignKey("paintings.id"))
    content = Column(Text)
    rating = Column(Integer)  # от 1 до 5

# app/models/user.py

from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))

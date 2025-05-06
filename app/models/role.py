# app/models/role.py

from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # admin, curator, guide, visitor

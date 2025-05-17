from sqlalchemy import Column, Integer, String
from .base import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # admin, curator, guide, visitor

    def __repr__(self):
        return f"<Role(name='{self.name}')>"
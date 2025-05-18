# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from .base import Base
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True)
#     telegram_id = Column(Integer, unique=True)
#     username = Column(String)
#     role_id = Column(Integer, ForeignKey('roles.id'))
#     role = relationship("Role")
#
#     def __repr__(self):
#         return f"<User(username='{self.username}', role='{self.role.name}')>"
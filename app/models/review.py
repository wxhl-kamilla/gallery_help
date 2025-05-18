# from sqlalchemy import Column, Integer, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from .base import Base
#
#
# class Review(Base):
#     __tablename__ = 'reviews'
#
#     id = Column(Integer, primary_key=True)
#     text = Column(Text, nullable=False)
#     rating = Column(Integer)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     painting_id = Column(Integer, ForeignKey('paintings.id'))
#
#     user = relationship("User", back_populates="reviews")
#     painting = relationship("Painting", back_populates="reviews")
#
#     def __repr__(self):
#         return f"<Review(id={self.id}, rating={self.rating})>"
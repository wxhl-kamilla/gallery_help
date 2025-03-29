from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Review(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    rating = sqlalchemy.Column(sqlalchemy.Integer)
    is_about_exhibition = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    painting_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('paintings.id'))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    painting = orm.relationship("Painting", back_populates='reviews')
    user = orm.relationship("User")

    def __repr__(self):
        return f'<Review> {self.id} by User#{self.user_id}'
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Painting(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'paintings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    year = sqlalchemy.Column(sqlalchemy.Integer)
    style = sqlalchemy.Column(sqlalchemy.String(100))
    description = sqlalchemy.Column(sqlalchemy.Text)
    image_url = sqlalchemy.Column(sqlalchemy.String(255))
    artist_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('artists.id'))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now, onupdate=datetime.now)

    artist = orm.relationship("Artist", back_populates='paintings')
    reviews = orm.relationship("Review", back_populates='painting')

    def __repr__(self):
        return f'<Painting> {self.id} {self.title}'
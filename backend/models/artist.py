from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Artist(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'artists'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    birth_date = sqlalchemy.Column(sqlalchemy.Date)
    death_date = sqlalchemy.Column(sqlalchemy.Date)
    country = sqlalchemy.Column(sqlalchemy.String(100))
    biography = sqlalchemy.Column(sqlalchemy.Text)
    style = sqlalchemy.Column(sqlalchemy.String(100))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now, onupdate=datetime.now)

    paintings = orm.relationship("Painting", back_populates='artist')

    def __repr__(self):
        return f'<Artist> {self.id} {self.name}'
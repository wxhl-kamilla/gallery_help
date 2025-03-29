from enum import Enum
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase

class UserRole(Enum):
    VISITOR = "Посетитель"
    GUIDE = "Экскурсовод"
    CURATOR = "Куратор"
    ADMIN = "Администратор"

class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String(50))
    full_name = sqlalchemy.Column(sqlalchemy.String(100))
    role = sqlalchemy.Column(sqlalchemy.Enum(UserRole), default=UserRole.VISITOR)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_admin(self):
        return self.role == UserRole.ADMIN

    def __repr__(self):
        return f"<User {self.telegram_id} {self.role.value}>"
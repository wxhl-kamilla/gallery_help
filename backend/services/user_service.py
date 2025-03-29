from backend.models.user import User, UserRole
from backend.models.db_session import create_session


class UserService:
    @staticmethod
    def get_or_create(telegram_id: int, username: str = None, full_name: str = None) -> User:
        """Создает или возвращает существующего пользователя"""
        session = create_session()
        user = session.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                full_name=full_name
            )
            session.add(user)
            session.commit()

        session.close()
        return user

    @staticmethod
    def change_role(telegram_id: int, new_role: UserRole) -> bool:
        """Изменяет роль пользователя (только для админов)"""
        session = create_session()
        user = session.query(User).filter(User.telegram_id == telegram_id).first()

        if user:
            user.role = new_role
            session.commit()
            session.close()
            return True

        session.close()
        return False
from typing import Optional

from sqlalchemy import select

from backend.models.user import User, UserRole
from backend.models.db_session import async_session

class AuthService:
    @staticmethod
    async def get_user(telegram_id: int) -> Optional[User]:
        """Асинхронно получает пользователя из БД"""
        async with async_session() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id)
            return result.scalar_one_or_none()

    @staticmethod
    async def is_admin(telegram_id: int) -> bool:
        """Проверяет, является ли пользователь админом"""
        user = await AuthService.get_user(telegram_id)
        return user is not None and user.role == UserRole.ADMIN

    @staticmethod
    async def is_curator(telegram_id: int) -> bool:
        """Проверяет, является ли пользователь куратором"""
        user = await AuthService.get_user(telegram_id)
        return user is not None and user.role in [UserRole.CURATOR, UserRole.ADMIN]
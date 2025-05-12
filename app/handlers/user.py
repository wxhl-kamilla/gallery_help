from aiogram import Router
from aiogram.types import Message
from app.database import async_session_maker
from app.models.user import User
from sqlalchemy import select

router = Router()

@router.message()
async def register_user(message: Message):
    async with async_session_maker() as session:
        user_id = message.from_user.id
        stmt = select(User).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            new_user = User(
                telegram_id=user_id,
                username=message.from_user.username,
                role="visitor"
            )
            session.add(new_user)
            await session.commit()
            await message.answer("👋 Добро пожаловать! Вы зарегистрированы как посетитель.")

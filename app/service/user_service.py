# from sqlalchemy import select
# from app.database import get_session
# from app.models.user import User
#
# DEFAULT_ROLE = "visitor"
#
# async def get_or_create_user_role(user_id: int, full_name: str) -> str:
#     async for session in get_session():
#         result = await session.execute(select(User).where(User.telegram_id == user_id))
#         user = result.scalars().first()
#
#         if user:
#             return user.role
#
#         # Создаем нового пользователя
#         new_user = User(telegram_id=user_id, full_name=full_name, role=DEFAULT_ROLE)
#         session.add(new_user)
#         await session.commit()
#         return new_user.role

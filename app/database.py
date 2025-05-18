# # app/database.py
#
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy.orm import sessionmaker
#
# DATABASE_URL = "sqlite+aiosqlite:///gallery.db"
#
# engine = create_async_engine(DATABASE_URL, echo=False)
# async_session = async_sessionmaker(engine, expire_on_commit=False)
#
# # Используем как dependency при вызовах
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session

# init_db.py

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import Base
from app.models import role, user, artist, painting, review

DATABASE_URL = "sqlite+aiosqlite:///gallery.db"

async def init_models():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())

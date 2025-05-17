# bot.py

import asyncio
from aiogram import Bot, Dispatcher
from config_k import BOT_TOKEN
from app.handlers import setup_routers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем все хендлеры
dp.include_router(setup_routers())

from app.handlers import start
dp.include_router(start.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

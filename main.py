import logging
from telegram.ext import Application
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from backend.handlers import start, menu, artist_info

# Инициализация логгера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Основная асинхронная функция для запуска бота
async def main(painting_info=None, leave_review=None):
    # Создаем объект Application
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("artist_info", artist_info))
    application.add_handler(CommandHandler("painting_info", painting_info))
    application.add_handler(CommandHandler("leave_review", leave_review))

    # Добавляем команды для админов
    application.add_handler(CommandHandler("add_artist", add_artist))
    application.add_handler(CommandHandler("add_painting", add_painting))

    # Запуск бота
    await application.run_polling()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())

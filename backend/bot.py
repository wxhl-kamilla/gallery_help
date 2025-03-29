from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from config import Config
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот картинной галереи.",
        reply_markup=None
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /help"""
    help_text = (
        "🖼 <b>Доступные команды:</b>\n\n"
        "/start - начать работу\n"
        "/help - эта справка\n"
        "/artists - список художников\n"
        "/painting [id] - информация о картине\n\n"
        "Просто отправьте фото картины для распознавания!"
    )
    await update.message.reply_html(help_text)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка присланных фотографий"""
    photo = update.message.photo[-1]
    file = await photo.get_file()

    await update.message.reply_text(
        "🔄 Обрабатываю изображение...",
        reply_to_message_id=update.message.message_id
    )

    # Здесь будет логика распознавания картины
    result = "Картина: «Звездная ночь»\nХудожник: Ван Гог (1889)"

    await update.message.reply_text(result)


def main() -> None:
    """Запуск бота"""
    # Создаем экземпляр Application
    application = Application.builder().token("7676755249:AAGQm0NwIgD6kCPyTtbJBI5WjsA3AcX5dps").build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Обработчик фотографий
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запускаем бота в режиме polling
    application.run_polling()


if __name__ == "__main__":
    main()
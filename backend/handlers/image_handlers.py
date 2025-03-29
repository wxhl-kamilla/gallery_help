from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from backend.services.painting_service import PaintingService
# from services.s3_service import S3Service


def handle_image(update: Update, context: CallbackContext):
    """Обработка загруженных изображений для поиска картин"""
    photo = update.message.photo[-1]
    file = context.bot.get_file(photo.file_id)

    # Сохраняем во временный файл
    image_path = "static/temp/received.jpg"
    file.download(image_path)

    # Здесь должна быть логика распознавания изображения
    # Временная заглушка:
    painting = PaintingService.get_random()

    if painting:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Возможно, это: {painting.title} ({painting.artist.name})"
        )
    else:
        update.message.reply_text("Не удалось распознать картину")


def setup_image_handlers(dispatcher):
    dispatcher.add_handler(MessageHandler(filters.photo, handle_image))
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from backend.services.artist_service import ArtistService
from backend.services.painting_service import PaintingService


def list_artists(update: Update, context: CallbackContext):
    """Показать список художников"""
    artists = ArtistService.get_all()
    if not artists:
        update.message.reply_text("В галерее пока нет художников.")
        return

    message = "🎨 Художники в галерее:\n\n" + \
              "\n".join(f"{i + 1}. {artist.name}" for i, artist in enumerate(artists))

    update.message.reply_text(message)


def show_painting(update: Update, context: CallbackContext):
    """Показать информацию о картине"""
    try:
        painting_id = int(context.args[0])
        painting = PaintingService.get_by_id(painting_id)

        if not painting:
            update.message.reply_text("Картина не найдена.")
            return

        message = (
            f"🖼 <b>{painting.title}</b>\n\n"
            f"👨‍🎨 Художник: {painting.artist.name}\n"
            f"📅 Год создания: {painting.year}\n"
            f"🎭 Стиль: {painting.style}\n\n"
            f"{painting.description}"
        )

        update.message.reply_text(message, parse_mode='HTML')

    except (IndexError, ValueError):
        update.message.reply_text("Используйте: /painting <ID_картины>")


def setup_content_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("artists", list_artists))
    dispatcher.add_handler(CommandHandler("painting", show_painting))
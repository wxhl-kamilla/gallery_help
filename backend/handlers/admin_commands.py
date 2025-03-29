from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from services.user_service import UserService
from models.user import UserRole
from utils.decorators import admin_required, curator_required


@admin_required
def set_role(update: Update, context: CallbackContext):
    """Изменить роль пользователя (только для админов)"""
    try:
        user_id = int(context.args[0])
        role_name = context.args[1].upper()
        new_role = UserRole[role_name]

        if UserService.change_role(user_id, new_role):
            update.message.reply_text(f"✅ Роль пользователя изменена на {new_role.value}")
        else:
            update.message.reply_text("❌ Пользователь не найден")

    except (IndexError, KeyError, ValueError):
        update.message.reply_text("Использование: /set_role <user_id> <VISITOR|GUIDE|CURATOR|ADMIN>")


@curator_required
def add_artist(update: Update, context: CallbackContext):
    """Добавить нового художника (для кураторов и админов)"""
    # Здесь можно реализовать ConversationHandler для пошагового ввода
    update.message.reply_text("Введите команду в формате: /add_artist <Имя> [Страна] [Годы жизни]")


def setup_admin_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("set_role", set_role))
    dispatcher.add_handler(CommandHandler("add_artist", add_artist))
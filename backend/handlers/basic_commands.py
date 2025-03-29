from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from backend.services.user_service import UserService

def start(update: Update, context: CallbackContext):
    """Обработка команды /start - регистрация пользователя"""
    user = update.effective_user
    db_user = UserService.get_or_create(
        telegram_id=user.id,
        username=user.username,
        full_name=user.full_name
    )

    welcome_msg = (
        f"🎨 Добро пожаловать в галерею, {user.full_name}!\n\n"
        f"Ваша роль: {db_user.role.value}\n\n"
        "Основные команды:\n"
        "/artists - список художников\n"
        "/paintings - список картин\n"
        "/help - справка по командам"
    )

    update.message.reply_text(welcome_msg)

def help_command(update: Update, context: CallbackContext):
    """Обработка команды /help"""
    help_text = (
        "📚 Доступные команды:\n\n"
        "Для всех:\n"
        "/start - регистрация\n"
        "/artists - художники\n"
        "/painting <id> - информация о картине\n\n"
        "Для кураторов и админов:\n"
        "/add_artist - добавить художника\n"
        "/add_painting - добавить картину\n\n"
        "Только для админов:\n"
        "/set_role - изменить роль пользователя"
    )
    update.message.reply_text(help_text)

def setup_basic_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
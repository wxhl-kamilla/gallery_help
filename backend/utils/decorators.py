from telegram import Update
from functools import wraps
from backend.services.user_service import UserService
from backend.models.user import UserRole

def admin_required(func):
    """Декоратор для проверки прав администратора"""
    @wraps(func)
    def wrapped(update: Update, context, *args, **kwargs):
        user = UserService.get_by_telegram_id(update.effective_user.id)
        if not user or not user.is_admin():
            update.message.reply_text("❌ Только для администраторов")
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def curator_required(func):
    """Декоратор для проверки прав куратора"""
    @wraps(func)
    def wrapped(update: Update, context, *args, **kwargs):
        user = UserService.get_by_telegram_id(update.effective_user.id)
        if not user or not (user.is_admin() or user.role == UserRole.CURATOR):
            update.message.reply_text("❌ Недостаточно прав")
            return
        return func(update, context, *args, **kwargs)
    return wrapped
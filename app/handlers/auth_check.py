# from telegram import Update
# from telegram.ext import ContextTypes
# from functools import wraps
# from app.service.auth_service import AuthService
# from app.service.database import
#
#
# def admin_required(func):
#     @wraps(func)
#     async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
#         db = next(get_db())
#         auth_service = AuthService(db)
#
#         user = auth_service.get_user_by_telegram_id(update.effective_user.id)
#         if not user or not auth_service.is_admin(user):
#             await update.message.reply_text("🚫 У вас нет прав администратора!")
#             return
#
#         return await func(update, context, *args, **kwargs)
#
#     return wrapper
#
#
# def curator_required(func):
#     @wraps(func)
#     async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
#         db = next(get_db())
#         auth_service = AuthService(db)
#
#         user = auth_service.get_user_by_telegram_id(update.effective_user.id)
#         if not user or not (auth_service.is_admin(user) or auth_service.is_curator(user)):
#             await update.message.reply_text("🚫 Только кураторы и администраторы могут выполнять эту команду!")
#             return
#
#         return await func(update, context, *args, **kwargs)
#
#     return wrapper
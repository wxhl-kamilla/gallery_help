import base64
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import pandas as pd


# Настройки YandexGPT
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
IAM_TOKEN = "AQVNz7P5YQRTOidVd08ZLNbqfeKVUrFhareRXbCg"  # Замените на реальный
FOLDER_ID = "b1gc46r88aeb0jn8autn"   # Из Yandex Cloud
# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния диалога
WAITING_FOR_DESCRIPTION = 1
IN_CONVERSATION = 2


async def start_yanGPT(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /yanGPT"""
    await update.message.reply_text(
        "Привет! Ты можешь:\n"
        "1. Написать описание картины — я угадаю её название и автора. Обязательно используй слово 'описание'\n"
        "2. Просто поболтать со мной.\n\n"
        "Попробуй! Например: 'описание: Русский витязь перед камнем с предупреждением'"
    )
    context.user_data['state'] = IN_CONVERSATION


async def summ(user_text, painting_id):
    """доделать промт используя бд"""
    db = pd.read_excel("data/reviews.xlsx")
    if(db.shape[0] == 0):
        return
    prompt = "отзывы о картине:\n"
    for i in range(db[db['painting_id']==painting_id].shape[0]):
        prompt += f"{db[db['painting_id']==painting_id].iloc[0]['description']}\n"
    prompt +='суммаризуй отзывы и выдай итог'
    return await call_yandex_gpt(prompt)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текста и фото"""
    user_text = update.message.text
    if any(word in user_text.lower() for word in ["описане", "описание", "описанеи"]):
        response = await guess_painting(user_text)
    elif 'сумм' in user_text.lower():
        response = await summ(user_text)
    else:
        response = await generate_chat_response(user_text)

    await update.message.reply_text(response)

async def guess_painting(description: str) -> str:
    """Определение картины по описанию через Yandex GPT"""
    db = pd.read_excel("data/paintings.xlsx")
    prompt = "Ниже приведён список картин и их описаний. Скажи название той, которая максимально подходит под описание, данное пользователем\n"
    for i in range(db.shape[0]):
        prompt += f"{i + 1}. \"{db['title'][i]}\"\nОписание: {db['description'][i]}\n\n"
    prompt += f'вот вопрос и описание пользователя: {description}'
    return await call_yandex_gpt(prompt)

async def generate_chat_response(user_text: str) -> str:
    """Генерация ответа для диалога"""
    prompt = (
        f"Ты дружелюбный ИИ-помощник в Telegram. "
        f"Пользователь написал: '{user_text}'. "
        f"Ответь кратко и естественно (максимум 2 предложения)."
    )
    return await call_yandex_gpt(prompt)

async def call_yandex_gpt(prompt: str) -> str:
    """Запрос к Yandex GPT API"""
    headers = {
        "Authorization": f"Bearer {IAM_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "temperature": 0.5,
            "maxTokens": 200
        },
        "messages": [{"role": "user", "text": prompt}]
    }
    try:
        response = requests.post(YANDEX_API_URL, headers=headers, json=data).json()
        return response.get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "Ошибка обработки запроса.")
    except Exception as e:
        logger.error(f"Yandex GPT error: {e}")
        return "Упс, что-то пошло не так..."

def main():
    app = Application.builder().token("7676755249:AAGQm0NwIgD6kCPyTtbJBI5WjsA3AcX5dps").build()
    app.add_handler(CommandHandler("yanGPT", start_yanGPT))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

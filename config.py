import os
from dotenv import load_dotenv

# Загружаем переменные окружения из config.env
load_dotenv('config.env')

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Пути к файлам
EXCEL_FILES = {
    'artists': 'data/artists.xlsx',
    'paintings': 'data/paintings1.xlsx',
    'reviews': 'data/reviews.xlsx',
    'gallery_reviews': 'data/gallery_reviews.xlsx',
    'users': 'data/users.xlsx'
}

# Пути к папкам
UPLOAD_FOLDER = 'uploads'
QR_FOLDER = 'qr_codes'

# Роли пользователей
ROLES = {
    'admin': 'Администратор',
    'curator': 'Куратор',
    'guide': 'Экскурсовод',
    'visitor': 'Посетитель'
}

# Создаем папки, если они не существуют
for folder in [UPLOAD_FOLDER, QR_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder) 
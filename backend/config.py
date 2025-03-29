import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv('7676755249:AAGQm0NwIgD6kCPyTtbJBI5WjsA3AcX5dps')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///gallery.db')
    S3_BUCKET = os.getenv('S3_BUCKET')
    S3_KEY = os.getenv('S3_ACCESS_KEY')
    S3_SECRET = os.getenv('S3_SECRET_KEY')
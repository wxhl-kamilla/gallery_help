import cv2
import numpy as np
from detect import run
import pandas as pd
import qrcode
from PIL import Image
import os
from config import UPLOAD_FOLDER, QR_FOLDER

class ImageRecognition:
    def __init__(self):
        pass

    def recognize_painting(self, image_path):
        p_id = run(source=image_path)

        p_db = pd.read_excel("paintings1.xlsx")
        a_db = pd.read_excel("artists.xlsx")

        p_row = p_db[p_db['id'] == p_id].iloc[0]
        a_row = a_db[a_db['id'] == p_row['artist_id']].iloc[0]

        result = f"\"{p_row['title']}\" - {a_row['name']}, {p_row['year']}\n\n{p_row['description']}"
        return result

def generate_qr_code(painting_data, image_path):
    """Генерация QR-кода для картины"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Формируем данные для QR-кода
    qr_data = f"""
    Название: {painting_data['title']}
    Художник: {painting_data['artist_name']}
    Год: {painting_data['year']}
    Описание: {painting_data['description']}
    """
    
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Создаем изображение QR-кода
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Если есть изображение картины, добавляем его в QR-код
    if image_path and os.path.exists(os.path.join('images', image_path)):
        # Открываем изображение картины
        painting_img = Image.open(os.path.join('images', image_path))
        
        # Изменяем размер изображения картины с сохранением пропорций
        max_size = 400
        ratio = min(max_size/painting_img.width, max_size/painting_img.height)
        new_size = (int(painting_img.width * ratio), int(painting_img.height * ratio))
        painting_img = painting_img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Создаем новое изображение с QR-кодом и картиной
        qr_size = 400
        final_width = qr_size + new_size[0]
        final_height = max(qr_size, new_size[1])
        final_image = Image.new('RGB', (final_width, final_height), 'white')
        
        # Конвертируем QR-код в RGB
        qr_image = qr_image.convert('RGB')
        
        # Изменяем размер QR-кода
        qr_image = qr_image.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        # Вставляем QR-код в левую часть
        final_image.paste(qr_image, (0, 0))
        
        # Вставляем изображение картины в правую часть
        final_image.paste(painting_img, (qr_size, 0))
        
        # Сохраняем результат с максимальным качеством
        qr_path = os.path.join(QR_FOLDER, f"qr_{painting_data['id']}.png")
        final_image.save(qr_path, quality=100, optimize=False)
    else:
        # Если изображения нет, сохраняем только QR-код
        qr_path = os.path.join(QR_FOLDER, f"qr_{painting_data['id']}.png")
        qr_image.save(qr_path, quality=100, optimize=False)
    
    return qr_path

def save_uploaded_image(file_id, file_path):
    """Сохранение загруженного изображения"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    save_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.jpg")
    # TODO: Реализовать сохранение файла
    return save_path

def get_keyboard_markup(buttons):
    """Создание клавиатуры с кнопками"""
    from telebot import types
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        markup.add(types.KeyboardButton(button))
    return markup 
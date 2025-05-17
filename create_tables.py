import pandas as pd
import os
from config import EXCEL_FILES

def create_excel_files():
    # Создаем директорию data, если её нет
    if not os.path.exists('data'):
        os.makedirs('data')

    # Создаем таблицу пользователей
    users_df = pd.DataFrame(columns=['user_id', 'username', 'role'])
    users_df.to_excel(EXCEL_FILES['users'], index=False)

    # Создаем таблицу художников с примерами
    artists_data = [
        {
            'id': 1,
            'name': 'Леонардо да Винчи',
            'biography': 'Итальянский художник и ученый эпохи Возрождения',
            'style': 'Ренессанс'
        },
        {
            'id': 2,
            'name': 'Винсент Ван Гог',
            'biography': 'Нидерландский художник-постимпрессионист',
            'style': 'Постимпрессионизм'
        },
        {
            'id': 3,
            'name': 'Пабло Пикассо',
            'biography': 'Испанский художник, основоположник кубизма',
            'style': 'Кубизм'
        }
    ]
    artists_df = pd.DataFrame(artists_data)
    artists_df.to_excel(EXCEL_FILES['artists'], index=False)

    # Создаем таблицу картин с примерами
    paintings_data = [
        {
            'id': 1,
            'title': 'Мона Лиза',
            'artist_id': 1,
            'year': 1503,
            'description': 'Портрет женщины с загадочной улыбкой',
            'image_path': 'mona_lisa.jpg'
        },
        {
            'id': 2,
            'title': 'Звездная ночь',
            'artist_id': 2,
            'year': 1889,
            'description': 'Ночной пейзаж с кипарисами и звездным небом',
            'image_path': 'starry_night.jpg'
        },
        {
            'id': 3,
            'title': 'Герника',
            'artist_id': 3,
            'year': 1937,
            'description': 'Антивоенная картина, изображающая ужасы войны',
            'image_path': 'guernica.jpg'
        }
    ]
    paintings_df = pd.DataFrame(paintings_data)
    paintings_df.to_excel(EXCEL_FILES['paintings'], index=False)

    # Создаем таблицу отзывов
    reviews_df = pd.DataFrame(columns=['id', 'user_id', 'painting_id', 'rating', 'comment', 'date'])
    reviews_df.to_excel(EXCEL_FILES['reviews'], index=False)

    print("Excel файлы успешно созданы с примерами данных!")

if __name__ == '__main__':
    create_excel_files()
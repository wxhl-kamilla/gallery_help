import pandas as pd
from config import EXCEL_FILES
import os

class Database:
    def __init__(self):
        self._init_excel_files()

    def _init_excel_files(self):
        """Инициализация Excel файлов с базовой структурой"""
        # Создаем директорию data, если её нет
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Проверяем существование файлов и создаем их только если они не существуют
        if not os.path.exists(EXCEL_FILES['artists']):
            artists_df = pd.DataFrame(columns=['id', 'name', 'biography', 'style'])
            artists_df.to_excel(EXCEL_FILES['artists'], index=False)
        
        if not os.path.exists(EXCEL_FILES['paintings']):
            paintings_df = pd.DataFrame(columns=['id', 'title', 'artist_id', 'year', 'description', 'image_path'])
            paintings_df.to_excel(EXCEL_FILES['paintings'], index=False)
        
        if not os.path.exists(EXCEL_FILES['reviews']):
            reviews_df = pd.DataFrame(columns=['id', 'user_id', 'painting_id', 'rating', 'comment', 'date'])
            reviews_df.to_excel(EXCEL_FILES['reviews'], index=False)
        
        if not os.path.exists(EXCEL_FILES['gallery_reviews']):
            gallery_reviews_df = pd.DataFrame(columns=['id', 'user_id', 'rating', 'comment', 'date'])
            gallery_reviews_df.to_excel(EXCEL_FILES['gallery_reviews'], index=False)
        
        if not os.path.exists(EXCEL_FILES['users']):
            users_df = pd.DataFrame(columns=['user_id', 'role'])
            users_df.to_excel(EXCEL_FILES['users'], index=False)

    def get_user_role(self, user_id):
        """Получение роли пользователя"""
        users_df = pd.read_excel(EXCEL_FILES['users'])
        user = users_df[users_df['user_id'] == user_id]
        if user.empty:
            # Если пользователь не найден, добавляем его с ролью visitor
            self.add_user(user_id)
            return 'visitor'
        return user['role'].iloc[0]

    def add_user(self, user_id):
        """Добавление нового пользователя"""
        users_df = pd.read_excel(EXCEL_FILES['users'])
        if users_df[users_df['user_id'] == user_id].empty:
            new_user = pd.DataFrame({
                'user_id': [user_id],
                'role': ['visitor']
            })
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_excel(EXCEL_FILES['users'], index=False)
            return True
        return False

    def update_user_role(self, user_id, new_role):
        """Обновление роли пользователя"""
        users_df = pd.read_excel(EXCEL_FILES['users'])
        mask = users_df['user_id'] == user_id
        if not mask.any():
            # Если пользователь не найден, добавляем его с новой ролью
            self.add_user(user_id)
            users_df.loc[users_df['user_id'] == user_id, 'role'] = new_role
        else:
            users_df.loc[mask, 'role'] = new_role
        users_df.to_excel(EXCEL_FILES['users'], index=False)
        return True

    def get_artists(self):
        """Получение списка всех художников"""
        return pd.read_excel(EXCEL_FILES['artists'])

    def get_artist(self, artist_id):
        """Получение информации о конкретном художнике"""
        artists_df = pd.read_excel(EXCEL_FILES['artists'])
        return artists_df[artists_df['id'] == artist_id].iloc[0]

    def get_paintings(self):
        """Получение списка всех картин"""
        return pd.read_excel(EXCEL_FILES['paintings'])

    def get_painting(self, painting_id):
        """Получение информации о конкретной картине"""
        paintings_df = pd.read_excel(EXCEL_FILES['paintings'])
        return paintings_df[paintings_df['id'] == painting_id].iloc[0]

    def get_reviews(self, painting_id, page=1, per_page=5):
        """Получение отзывов о картине с пагинацией"""
        reviews_df = pd.read_excel(EXCEL_FILES['reviews'])
        users_df = pd.read_excel(EXCEL_FILES['users'])
        
        # Фильтруем отзывы по картине
        reviews = reviews_df[reviews_df['painting_id'] == painting_id].copy()
        
        # Проверяем наличие необходимых колонок
        if 'user_id' not in reviews.columns:
            reviews['user_id'] = None
        
        # Добавляем информацию о роли пользователя
        reviews = reviews.merge(
            users_df[['user_id', 'role']],
            on='user_id',
            how='left'
        )
        
        # Проверяем наличие колонки role и создаем её при необходимости
        if 'role' not in reviews.columns:
            reviews['role'] = 'visitor'
        else:
            reviews['role'] = reviews['role'].fillna('visitor')
        
        # Сортируем отзывы: сначала экскурсоводы, потом остальные
        reviews['is_guide'] = reviews['role'] == 'guide'
        reviews = reviews.sort_values(['is_guide', 'date'], ascending=[False, False])
        
        # Вычисляем общее количество страниц
        total_pages = (len(reviews) + per_page - 1) // per_page
        
        # Получаем отзывы для текущей страницы
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_reviews = reviews.iloc[start_idx:end_idx]
        
        return page_reviews, total_pages

    def add_review(self, user_id, painting_id, text, rating):
        """Добавить отзыв о картине"""
        try:
            reviews_df = pd.read_excel(EXCEL_FILES['reviews'])
            
            # Генерируем новый ID
            new_id = 1 if reviews_df.empty else reviews_df['id'].max() + 1
            
            # Получаем роль пользователя
            user_role = self.get_user_role(user_id)
            
            # Создаем новый отзыв
            new_review = pd.DataFrame([{
                'id': new_id,
                'user_id': user_id,
                'painting_id': painting_id,
                'text': text,
                'rating': rating,
                'role': user_role,
                'date': pd.Timestamp.now()
            }])
            
            # Добавляем отзыв в DataFrame
            reviews_df = pd.concat([reviews_df, new_review], ignore_index=True)
            
            # Сохраняем изменения
            reviews_df.to_excel(EXCEL_FILES['reviews'], index=False)
            return True
        except Exception as e:
            print(f"Error adding review: {e}")
            return False

    def get_gallery_reviews(self, page=1, per_page=5):
        """Получение отзывов о галерее с пагинацией"""
        reviews_df = pd.read_excel(EXCEL_FILES['gallery_reviews'])
        users_df = pd.read_excel(EXCEL_FILES['users'])
        
        # Создаем копию DataFrame с отзывами
        reviews = reviews_df.copy()
        
        # Проверяем наличие необходимых колонок
        if 'user_id' not in reviews.columns:
            reviews['user_id'] = None
        
        # Добавляем информацию о роли пользователя
        reviews = reviews.merge(
            users_df[['user_id', 'role']],
            on='user_id',
            how='left'
        )
        
        # Проверяем наличие колонки role и создаем её при необходимости
        if 'role' not in reviews.columns:
            reviews['role'] = 'visitor'
        else:
            reviews['role'] = reviews['role'].fillna('visitor')
        
        # Сортируем отзывы: сначала экскурсоводы, потом остальные, затем по дате
        reviews['is_guide'] = reviews['role'] == 'guide'
        reviews = reviews.sort_values(['is_guide', 'date'], ascending=[False, False])
        
        # Вычисляем общее количество страниц
        total_pages = (len(reviews) + per_page - 1) // per_page
        
        # Получаем отзывы для текущей страницы
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_reviews = reviews.iloc[start_idx:end_idx]
        
        return page_reviews, total_pages

    def add_gallery_review(self, user_id, text, rating):
        """Добавить отзыв о галерее"""
        try:
            reviews_df = pd.read_excel(EXCEL_FILES['gallery_reviews'])
            
            # Генерируем новый ID
            new_id = 1 if reviews_df.empty else reviews_df['id'].max() + 1
            
            # Получаем роль пользователя
            user_role = self.get_user_role(user_id)
            
            # Создаем новый отзыв
            new_review = pd.DataFrame([{
                'id': new_id,
                'user_id': user_id,
                'text': text,
                'rating': rating,
                'role': user_role,
                'date': pd.Timestamp.now()
            }])
            
            # Добавляем отзыв в DataFrame
            reviews_df = pd.concat([reviews_df, new_review], ignore_index=True)
            
            # Сохраняем изменения
            reviews_df.to_excel(EXCEL_FILES['gallery_reviews'], index=False)
            return True
        except Exception as e:
            print(f"Error adding gallery review: {e}")
            return False

    def get_painting_reviews(self, painting_id, page=1, per_page=5):
        """Получение отзывов о картине с пагинацией"""
        reviews_df = pd.read_excel(EXCEL_FILES['reviews'])
        users_df = pd.read_excel(EXCEL_FILES['users'])
        
        # Объединяем отзывы с информацией о пользователях
        reviews = reviews_df[reviews_df['painting_id'] == painting_id].merge(
            users_df[['user_id', 'role']],
            on='user_id',
            how='left'
        )
        
        # Сортируем отзывы: сначала экскурсоводы, потом остальные
        reviews['is_guide'] = reviews['role'] == 'guide'
        reviews = reviews.sort_values(['is_guide', 'date'], ascending=[False, False])
        
        # Вычисляем общее количество страниц
        total_pages = (len(reviews) + per_page - 1) // per_page
        
        # Получаем отзывы для текущей страницы
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_reviews = reviews.iloc[start_idx:end_idx]
        
        return page_reviews, total_pages

    def add_artist(self, artist_data):
        """Добавление нового художника"""
        try:
            artists_df = pd.read_excel(EXCEL_FILES['artists'])
            new_id = 1 if artists_df.empty else artists_df['id'].max() + 1
            
            new_artist = pd.DataFrame([{
                'id': new_id,
                'name': artist_data['name'],
                'biography': artist_data['biography'],
                'style': artist_data['style']
            }])
            
            artists_df = pd.concat([artists_df, new_artist], ignore_index=True)
            artists_df.to_excel(EXCEL_FILES['artists'], index=False)
            return True
        except Exception as e:
            print(f"Error adding artist: {e}")
            return False

    def edit_artist(self, artist_id, field, value):
        """Редактирование информации о художнике"""
        try:
            artists_df = pd.read_excel(EXCEL_FILES['artists'])
            if artist_id not in artists_df['id'].values:
                return False
            
            artists_df.loc[artists_df['id'] == artist_id, field] = value
            artists_df.to_excel(EXCEL_FILES['artists'], index=False)
            return True
        except Exception as e:
            print(f"Error editing artist: {e}")
            return False

    def delete_artist(self, artist_id):
        """Удаление художника"""
        try:
            artists_df = pd.read_excel(EXCEL_FILES['artists'])
            if artist_id not in artists_df['id'].values:
                return False
            
            # Удаляем художника
            artists_df = artists_df[artists_df['id'] != artist_id]
            artists_df.to_excel(EXCEL_FILES['artists'], index=False)
            
            # Удаляем связанные картины
            paintings_df = pd.read_excel(EXCEL_FILES['paintings'])
            paintings_df = paintings_df[paintings_df['artist_id'] != artist_id]
            paintings_df.to_excel(EXCEL_FILES['paintings'], index=False)
            
            return True
        except Exception as e:
            print(f"Error deleting artist: {e}")
            return False

    def add_painting(self, painting_data):
        """Добавление новой картины"""
        try:
            paintings_df = pd.read_excel(EXCEL_FILES['paintings'])
            new_id = 1 if paintings_df.empty else paintings_df['id'].max() + 1
            
            new_painting = pd.DataFrame([{
                'id': new_id,
                'title': painting_data['title'],
                'description': painting_data['description'],
                'year': painting_data['year'],
                'artist_id': painting_data['artist_id'],
                'image_path': painting_data['image_path']
            }])
            
            paintings_df = pd.concat([paintings_df, new_painting], ignore_index=True)
            paintings_df.to_excel(EXCEL_FILES['paintings'], index=False)
            return True
        except Exception as e:
            print(f"Error adding painting: {e}")
            return False

    def delete_review(self, review_id):
        """Удаление отзыва"""
        try:
            reviews_df = pd.read_excel(EXCEL_FILES['reviews'])
            if review_id not in reviews_df['id'].values:
                return False
            
            reviews_df = reviews_df[reviews_df['id'] != review_id]
            reviews_df.to_excel(EXCEL_FILES['reviews'], index=False)
            return True
        except Exception as e:
            print(f"Error deleting review: {e}")
            return False

    def delete_gallery_review(self, review_id):
        """Удалить отзыв о галерее"""
        try:
            reviews_df = pd.read_excel(EXCEL_FILES['gallery_reviews'])
            reviews_df = reviews_df[reviews_df['id'] != review_id]
            reviews_df.to_excel(EXCEL_FILES['gallery_reviews'], index=False)
            return True
        except Exception as e:
            print(f"Error deleting gallery review: {e}")
            return False

    def delete_painting(self, painting_id):
        """Удаление картины"""
        try:
            # Читаем файл с картинами
            paintings_df = pd.read_excel(EXCEL_FILES['paintings'])
            
            # Проверяем существование картины
            if painting_id not in paintings_df['id'].values:
                return False
            
            # Получаем информацию о картине для удаления изображения
            painting = paintings_df[paintings_df['id'] == painting_id].iloc[0]
            
            # Удаляем картину из DataFrame
            paintings_df = paintings_df[paintings_df['id'] != painting_id]
            
            # Сохраняем обновленный DataFrame
            paintings_df.to_excel(EXCEL_FILES['paintings'], index=False)
            
            # Удаляем отзывы о картине
            reviews_df = pd.read_excel(EXCEL_FILES['reviews'])
            reviews_df = reviews_df[reviews_df['painting_id'] != painting_id]
            reviews_df.to_excel(EXCEL_FILES['reviews'], index=False)
            
            # Удаляем изображение картины, если оно существует
            if 'image_path' in painting and pd.notna(painting['image_path']):
                try:
                    os.remove(painting['image_path'])
                except:
                    pass  # Игнорируем ошибки при удалении файла
            
            return True
        except Exception as e:
            print(f"Error in delete_painting: {e}")
            return False

    def edit_painting(self, painting_id, field, value):
        """Редактирование информации о картине"""
        try:
            paintings_df = pd.read_excel(EXCEL_FILES['paintings'])
            if painting_id not in paintings_df['id'].values:
                return False
            
            # Проверяем, что поле существует
            if field not in paintings_df.columns:
                return False
            
            # Обновляем значение
            paintings_df.loc[paintings_df['id'] == painting_id, field] = value
            
            # Сохраняем изменения
            paintings_df.to_excel(EXCEL_FILES['paintings'], index=False)
            return True
        except Exception as e:
            print(f"Error editing painting: {e}")
            return False 
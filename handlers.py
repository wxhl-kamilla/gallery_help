from telebot import types
from database import Database
from utilss import ImageRecognition, generate_qr_code, get_keyboard_markup
from config import ROLES, EXCEL_FILES, IAM_TOKEN, YANDEX_API_URL, FOLDER_ID
import os
import pandas as pd
from detect import run
import loadenv

class Handlers:
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.image_recognition = ImageRecognition()
        self.user_states = {}

    def start(self, message):
        """Обработчик команды /start"""
        user_id = message.from_user.id
        
        # Добавляем пользователя в базу (если его еще нет)
        self.db.add_user(user_id)
        
        # Создаем клавиатуру
        buttons = [
            "📚 Каталог художников",
            "🖼 Каталог картин",
            "🔍 Найти картину по фото",
            "📝 Отзывы о галерее",
            "❓ Помощь"
        ]
        
        markup = get_keyboard_markup(buttons)
        
        welcome_text = """
        Добро пожаловать в Галерею Искусств! 🎨
        
        Я помогу вам узнать больше о картинах и художниках.
        Используйте кнопки меню для навигации.
        
        Доступные команды:
        /start - Начать работу с ботом
        /help - Показать справку
        /gallery_reviews - Показать отзывы о галерее
        /add_gallery_review - Оставить отзыв о галерее
        """
        
        self.bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

    def request_role(self, message):
        """Обработчик запроса на получение роли"""
        user_id = message.from_user.id
        current_role = self.db.get_user_role(user_id)
        
        if current_role in ['admin', 'curator']:
            self.bot.reply_to(message, "У вас уже есть привилегированная роль.")
            return
        
        # Получаем список администраторов
        users_df = pd.read_excel(EXCEL_FILES['users'])
        admins = users_df[users_df['role'] == 'admin']
        
        # Отправляем запрос администраторам
        admin_message = f"""
        Новый запрос на получение роли:
        Пользователь: @{message.from_user.username}
        ID: {user_id}
        Текущая роль: {current_role}
        """
        
        # Отправляем сообщение всем администраторам
        for _, admin in admins.iterrows():
            try:
                self.bot.send_message(admin['user_id'], admin_message)
            except:
                continue
        
        self.bot.reply_to(message, "Ваш запрос отправлен администраторам.")

    def show_artists(self, message, page=1):
        """Показать каталог художников с пагинацией"""
        artists = self.db.get_artists()
        if artists.empty:
            self.bot.reply_to(message, "В каталоге пока нет художников.")
            return
        
        # Вычисляем общее количество страниц
        per_page = 5
        total_pages = (len(artists) + per_page - 1) // per_page
        
        # Получаем художников для текущей страницы
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_artists = artists.iloc[start_idx:end_idx]
        
        # Создаем инлайн-кнопки для каждого художника
        markup = types.InlineKeyboardMarkup()
        for _, artist in page_artists.iterrows():
            button = types.InlineKeyboardButton(
                text=f"🎨 {artist['name']}",
                callback_data=f"artist_{artist['id']}"
            )
            markup.add(button)
        
        # Добавляем кнопки навигации
        nav_buttons = []
        if page > 1:
            nav_buttons.append(types.InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"artists_page_{page-1}"
            ))
        if page < total_pages:
            nav_buttons.append(types.InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"artists_page_{page+1}"
            ))
        if nav_buttons:
            markup.add(*nav_buttons)
        
        text = f"Выберите художника из списка (страница {page} из {total_pages}):"
        
        if isinstance(message, types.CallbackQuery):
            self.bot.edit_message_text(
                text,
                message.message.chat.id,
                message.message.message_id,
                reply_markup=markup
            )
        else:
            self.bot.send_message(
                message.chat.id,
                text,
                reply_markup=markup
            )

    def show_artist_details(self, call):
        """Показать детальную информацию о художнике"""
        artist_id = int(call.data.split('_')[1])
        artist = self.db.get_artist(artist_id)
        
        text = f"""
🎨 Художник: {artist['name']}
📝 Биография: {artist['biography']}
🎭 Стиль: {artist['style']}
        """
        
        # Создаем кнопку для просмотра картин художника
        markup = types.InlineKeyboardMarkup()
        paintings_button = types.InlineKeyboardButton(
            text="🖼 Посмотреть картины",
            callback_data=f"artist_paintings_{artist_id}"
        )
        markup.add(paintings_button)
        
        self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    def show_paintings(self, message, page=1):
        """Показать каталог картин с пагинацией"""
        paintings = self.db.get_paintings()
        if paintings.empty:
            self.bot.reply_to(message, "В каталоге пока нет картин.")
            return
        
        # Вычисляем общее количество страниц
        per_page = 5
        total_pages = (len(paintings) + per_page - 1) // per_page
        
        # Получаем картины для текущей страницы
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_paintings = paintings.iloc[start_idx:end_idx]
        
        # Создаем инлайн-кнопки для каждой картины
        markup = types.InlineKeyboardMarkup()
        for _, painting in page_paintings.iterrows():
            button = types.InlineKeyboardButton(
                text=f"🖼 {painting['title']}",
                callback_data=f"painting_{painting['id']}"
            )
            markup.add(button)
        
        # Добавляем кнопки навигации
        nav_buttons = []
        if page > 1:
            nav_buttons.append(types.InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"paintings_page_{page-1}"
            ))
        if page < total_pages:
            nav_buttons.append(types.InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"paintings_page_{page+1}"
            ))
        if nav_buttons:
            markup.add(*nav_buttons)
        
        text = f"Выберите картину из списка (страница {page} из {total_pages}):"
        
        if isinstance(message, types.CallbackQuery):
            self.bot.edit_message_text(
                text,
                message.message.chat.id,
                message.message.message_id,
                reply_markup=markup
            )
        else:
            self.bot.send_message(
                message.chat.id,
                text,
                reply_markup=markup
            )

    def show_painting_details(self, call):
        """Показать детали картины"""
        try:
            # Получаем ID картины из callback данных
            data_parts = call.data.split('_')
            
            # Если это запрос на возврат к списку картин
            if call.data == "paintings":
                self.show_paintings(call.message)
                return
            
            if len(data_parts) < 2:
                return
                
            # Инициализируем переменные
            painting_id = None
            page = 1
                
            if data_parts[0] == 'painting':
                if len(data_parts) == 2:  # Формат: painting_1
                    try:
                        painting_id = int(data_parts[1])
                    except ValueError:
                        return
                elif len(data_parts) >= 3 and data_parts[1] == 'reviews':
                    try:
                        painting_id = int(data_parts[2])
                        if len(data_parts) > 3:
                            page = int(data_parts[3])
                    except ValueError:
                        return
                else:
                    return
            else:
                return
                
            # Получаем информацию о картине
            painting = self.db.get_painting(painting_id)
            if painting is None:
                return
            
            # Получаем отзывы с пагинацией
            reviews, total_pages = self.db.get_reviews(painting_id, page=page)
            
            # Формируем сообщение с информацией о картине
            message = f"🎨 {painting['title']}\n\n"
            message += f"📝 Описание: {painting['description']}\n"
            message += f"📅 Год создания: {painting['year']}\n"
            
            # Добавляем отзывы
            if not reviews.empty:
                message += "\n📝 Отзывы:\n"
                for _, review in reviews.iterrows():
                    role = review.get('role', 'visitor')
                    role_emoji = '👨‍🏫' if role == 'guide' else '👤'
                    message += f"\n{role_emoji} {review['text']}\n"
                    message += f"⭐️ Оценка: {review['rating']}/5\n"
                    message += f"📅 {review['date'].strftime('%d.%m.%Y')}\n"
            
            # Создаем клавиатуру
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            
            # Добавляем кнопки навигации по отзывам
            if total_pages > 1:
                nav_buttons = []
                if page > 1:
                    nav_buttons.append(types.InlineKeyboardButton(
                        "◀️", callback_data=f"painting_reviews_{painting_id}_{page-1}"
                    ))
                if page < total_pages:
                    nav_buttons.append(types.InlineKeyboardButton(
                        "▶️", callback_data=f"painting_reviews_{painting_id}_{page+1}"
                    ))
                if nav_buttons:
                    keyboard.add(*nav_buttons)
            
            # Добавляем кнопки действий
            keyboard.add(
                types.InlineKeyboardButton("📝 Оставить отзыв", callback_data=f"review_{painting_id}"),
                types.InlineKeyboardButton("📱 Получить QR-код", callback_data=f"qr_{painting_id}")
            )
            keyboard.add(types.InlineKeyboardButton("🔙 К списку картин", callback_data="paintings"))
            
            # Проверяем наличие изображения
            image_path = painting.get('image_path')
            
            if image_path and pd.notna(image_path):
                # Формируем полный путь к изображению
                full_image_path = os.path.join('images', image_path)
                
                try:
                    # Проверяем существование файла
                    if not os.path.exists(full_image_path):
                        raise FileNotFoundError(f"Image file not found: {full_image_path}")
                    
                    with open(full_image_path, 'rb') as photo:
                        self.bot.send_photo(
                            call.message.chat.id,
                            photo,
                            caption=message,
                            reply_markup=keyboard
                        )
                    
                    # Удаляем предыдущее сообщение
                    self.bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    # Если не удалось отправить фото, отправляем только текст
                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=message,
                        reply_markup=keyboard
                    )
            else:
                # Если нет пути к изображению, отправляем только текст
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=message,
                    reply_markup=keyboard
                )
                
        except Exception:
            return

    def show_artist_paintings(self, call):
        """Показать картины конкретного художника"""
        artist_id = int(call.data.split('_')[2])
        paintings = self.db.get_paintings()
        artist_paintings = paintings[paintings['artist_id'] == artist_id]
        
        if artist_paintings.empty:
            self.bot.answer_callback_query(
                call.id,
                "У этого художника пока нет картин в каталоге."
            )
            return
        
        # Создаем инлайн-кнопки для картин художника
        markup = types.InlineKeyboardMarkup()
        for _, painting in artist_paintings.iterrows():
            button = types.InlineKeyboardButton(
                text=f"🖼 {painting['title']}",
                callback_data=f"painting_{painting['id']}"
            )
            markup.add(button)
        
        self.bot.edit_message_text(
            "Картины художника:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    def handle_photo(self, message):
        """Обработка фотографии для поиска картины"""
        
        file_info = self.bot.get_file(message.photo[0].file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)
        with open("image.jpg","wb") as f:
            f.write(downloaded_file)
        p_id = run(source="image.jpg")

        if(p_id is None):
            self.bot.reply_to(message,"Ошибка, попробуйте отправить фото как файл")
            return

        p_db = pd.read_excel("data/paintings.xlsx")
        a_db = pd.read_excel("data/artists.xlsx")

        p_row = p_db[p_db['id'] == p_id].iloc[0]
        a_row = a_db[a_db['id'] == p_row['artist_id']].iloc[0]

        result = f"\"{p_row['title']}\" - {a_row['name']}, {p_row['year']}\n\n{p_row['description']}"
        self.bot.reply_to(message,result)

    def add_review(self, message):
        """Добавление отзыва"""
        # TODO: Реализовать добавление отзыва
        pass

    def help_command(self, message):
        """Показать справку в зависимости от роли пользователя"""
        user_id = message.from_user.id
        user_role = self.db.get_user_role(user_id)
        
        if user_role in ['admin', 'curator']:
            help_text = """
🤖 Справка по командам для администраторов и кураторов:

Основные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/request_role - Запросить роль куратора или экскурсовода
/add_gallery_review - Оставить отзыв о галерее

Команды управления:
/add_artist - Добавить нового художника
/edit_artist - Редактировать информацию о художнике
/delete_artist - Удалить художника
/add_painting - Добавить новую картину
/edit_painting - Редактировать информацию о картине
/delete_painting - Удалить картину
/delete_review - Удалить отзыв о картине
/delete_gallery_review - Удалить отзыв о галерее

Основные функции:
- Просмотр каталога художников
- Просмотр каталога картин
- Поиск картины по фотографии
- Оставить отзывов
- Генерация QR-кодов для картин
"""
        else:
            help_text = """
🤖 Справка по командам для посетителей:

Основные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/add_gallery_review - Оставить отзыв о галерее

Основные функции:
- Просмотр каталога художников
- Просмотр каталога картин
- Поиск картины по фотографии
- Оставить отзывов
- Генерация QR-кодов для картин
"""
        
        self.bot.reply_to(message, help_text)

    def handle_review_callback(self, call):
        """Обработка нажатия на кнопку 'Оставить отзыв'"""
        painting_id = int(call.data.split('_')[1])
        user_id = call.from_user.id
        
        # Проверяем, не оставлял ли пользователь уже отзыв
        reviews_df = pd.read_excel(EXCEL_FILES['reviews'])
        if not reviews_df[(reviews_df['user_id'] == user_id) & 
                         (reviews_df['painting_id'] == painting_id)].empty:
            self.bot.answer_callback_query(
                call.id,
                "Вы уже оставили отзыв на эту картину",
                show_alert=True
            )
            return
        
        # Сохраняем состояние пользователя
        self.user_states[user_id] = {
            'state': 'waiting_review',
            'painting_id': painting_id
        }
        
        # Создаем кнопки для оценки
        markup = types.InlineKeyboardMarkup()
        for rating in range(1, 6):
            button = types.InlineKeyboardButton(
                text=f"{'⭐' * rating}",
                callback_data=f"rating_{rating}"
            )
            markup.add(button)
        
        # Отправляем новое сообщение вместо редактирования
        self.bot.send_message(
            call.message.chat.id,
            "Оцените картину от 1 до 5 звезд:",
            reply_markup=markup
        )
        
        # Отвечаем на callback query
        self.bot.answer_callback_query(call.id)

    def handle_rating_callback(self, call):
        """Обработка выбора оценки"""
        rating = int(call.data.split('_')[1])
        user_id = call.from_user.id
        
        if user_id not in self.user_states:
            self.bot.answer_callback_query(call.id, "Произошла ошибка. Попробуйте снова.")
            return
        
        # Сохраняем оценку
        self.user_states[user_id]['rating'] = rating
        
        # Запрашиваем текстовый отзыв
        self.bot.edit_message_text(
            "Теперь напишите ваш отзыв о картине:",
            call.message.chat.id,
            call.message.message_id
        )
        
        # Меняем состояние
        self.user_states[user_id]['state'] = 'waiting_comment'

    


    def summ(user_text):
        """Суммируй отзывы"""
        review_db = pd.read_excel("data/reviews.xlsx")
        gallery_db = pd.read_excel("data/gallery_reviews.xlsx")
        paintings_db = pd.read_excel("data/paintings.xlsx")
        prompt = "тебе даются отзывы о картинной галерее в целом, и картинах, представленных на ней, по отдельности. Также тебе даётся сообщение пользователя с просьбой обобщить отзывы по галерее или по какой либо картине в частности. Отзывы о картинах:\n"
        for i in range(review_db.shape[0]):
            prompt += f"{paintings_db[paintings_db['id']==review_db.loc[i]['painting_id']].iloc[0]['title']}: {review_db.loc[i]['text']}\n"
        prompt += "Отзывы о галерее:\n"
        for i in range(gallery_db.shape[0]):
            prompt += f"{gallery_db.loc[i]['text']}\n"
        prompt += f'Сообщение пользователя: {user_text}'
        return call_yandex_gpt(prompt)


    def handle_message(message):
        """Обработка текста и фото"""
        user_text = message.text
        if any(word in user_text.lower() for word in ["описане", "описание", "описанеи"]):
            response = guess_painting(user_text)
        elif 'сумм' in user_text.lower():
            response = summ(user_text)
        else:
            response = generate_chat_response(user_text)
            
        self.bot.reply_to(message, response)

    def guess_painting(description: str) -> str:
        """Определение картины по описанию через Yandex GPT"""
        db = pd.read_excel("data/paintings.xlsx")
        prompt = ""
        for i in range(db.shape[0]):
            prompt += f"{i + 1}. \"{db['title'][i]}\"\nОписание: {db['description'][i]}\n\n"
        prompt += f'вот вопрос и описание пользователя: {description}'
        return call_yandex_gpt(prompt)

    def generate_chat_response(user_text: str) -> str:
        """Генерация ответа для диалога"""
        prompt = (
            f"Ты дружелюбный ИИ-помощник в Telegram. "
            f"Пользователь написал: '{user_text}'. "
            f"Ответь кратко и естественно (максимум 2 предложения)."
        )
        return call_yandex_gpt(prompt)

    def call_yandex_gpt(prompt: str) -> str:
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
            return "Упс, что-то пошло не так..."

    def handle_review_text(self, message):
        """Обработка текстового отзыва"""
        user_id = message.from_user.id
        
        if user_id not in self.user_states or self.user_states[user_id]['state'] != 'waiting_comment':
            return
        
        # Получаем сохраненные данные
        painting_id = self.user_states[user_id]['painting_id']
        rating = self.user_states[user_id]['rating']
        comment = message.text
        
        # Добавляем отзыв в базу
        if self.db.add_review(user_id, painting_id, comment, rating):
            self.bot.reply_to(message, "Спасибо за ваш отзыв! 🌟")
        else:
            self.bot.reply_to(message, "Произошла ошибка при сохранении отзыва. Попробуйте позже.")
        
        # Очищаем состояние пользователя
        del self.user_states[user_id]

    def handle_qr_callback(self, call):
        """Обработка нажатия на кнопку 'Получить QR-код'"""
        painting_id = int(call.data.split('_')[1])
        painting = self.db.get_painting(painting_id)
        artist = self.db.get_artist(painting['artist_id'])
        
        # Формируем данные для QR-кода
        painting_data = {
            'id': painting['id'],
            'title': painting['title'],
            'artist_name': artist['name'],
            'year': painting['year'],
            'description': painting['description']
        }
        
        # Генерируем QR-код
        qr_path = generate_qr_code(painting_data, painting['image_path'])
        
        if qr_path and os.path.exists(qr_path):
            # Отправляем QR-код
            with open(qr_path, 'rb') as qr_file:
                self.bot.send_photo(
                    call.message.chat.id,
                    qr_file,
                    caption=f"QR-код для картины '{painting['title']}'"
                )
        else:
            self.bot.answer_callback_query(
                call.id,
                "Ошибка при генерации QR-кода",
                show_alert=True
            )

    def show_gallery_reviews(self, message, page=1):
        """Показать отзывы о галерее"""
        reviews, total_pages = self.db.get_gallery_reviews(page)
        
        if reviews.empty:
            self.bot.reply_to(message, "Пока нет отзывов о галерее.")
            return
        
        # Формируем текст с отзывами
        text = f"📝 Отзывы о галерее (страница {page} из {total_pages}):\n\n"
        for _, review in reviews.iterrows():
            if review['role'] == 'guide':
                text += f"👨‍🏫 *Отзыв экскурсовода*\n"
            text += f"{'⭐' * review['rating']}\n{review['text']}\n\n"
        
        # Создаем кнопки навигации
        markup = types.InlineKeyboardMarkup()
        nav_buttons = []
        if page > 1:
            nav_buttons.append(types.InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"gallery_reviews_{page-1}"
            ))
        if page < total_pages:
            nav_buttons.append(types.InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"gallery_reviews_{page+1}"
            ))
        if nav_buttons:
            markup.add(*nav_buttons)
        
        # Добавляем кнопку для оставления отзыва
        add_review_button = types.InlineKeyboardButton(
            text="📝 Оставить отзыв",
            callback_data="add_gallery_review"
        )
        markup.add(add_review_button)
        
        if isinstance(message, types.CallbackQuery):
            self.bot.edit_message_text(
                text,
                message.message.chat.id,
                message.message.message_id,
                reply_markup=markup,
                parse_mode='Markdown'
            )
        else:
            self.bot.send_message(
                message.chat.id,
                text,
                reply_markup=markup,
                parse_mode='Markdown'
            )

    def handle_gallery_review_callback(self, call):
        """Обработка нажатия на кнопку 'Оставить отзыв о галерее'"""
        user_id = call.from_user.id
        
        # Проверяем, не оставлял ли пользователь уже отзыв
        reviews_df = pd.read_excel(EXCEL_FILES['gallery_reviews'])
        if not reviews_df[reviews_df['user_id'] == user_id].empty:
            self.bot.answer_callback_query(
                call.id,
                "Вы уже оставили отзыв о галерее",
                show_alert=True
            )
            return
        
        # Сохраняем состояние пользователя
        self.user_states[user_id] = {
            'state': 'waiting_gallery_review'
        }
        
        # Создаем кнопки для оценки
        markup = types.InlineKeyboardMarkup()
        for rating in range(1, 6):
            button = types.InlineKeyboardButton(
                text=f"{'⭐' * rating}",
                callback_data=f"gallery_rating_{rating}"
            )
            markup.add(button)
        
        self.bot.edit_message_text(
            "Оцените галерею от 1 до 5 звезд:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    def handle_gallery_rating_callback(self, call):
        """Обработка выбора оценки для отзыва о галерее"""
        rating = int(call.data.split('_')[2])
        user_id = call.from_user.id
        
        if user_id not in self.user_states:
            self.bot.answer_callback_query(call.id, "Произошла ошибка. Попробуйте снова.")
            return
        
        # Сохраняем оценку
        self.user_states[user_id]['rating'] = rating
        
        # Запрашиваем текстовый отзыв
        self.bot.edit_message_text(
            "Теперь напишите ваш отзыв о галерее:",
            call.message.chat.id,
            call.message.message_id
        )
        
        # Меняем состояние
        self.user_states[user_id]['state'] = 'waiting_gallery_comment'

    def handle_gallery_review_text(self, message):
        """Обработка текстового отзыва о галерее"""
        user_id = message.from_user.id
        
        if user_id not in self.user_states or self.user_states[user_id]['state'] != 'waiting_gallery_comment':
            return
        
        # Получаем сохраненные данные
        rating = self.user_states[user_id]['rating']
        comment = message.text
        
        # Добавляем отзыв в базу
        if self.db.add_gallery_review(user_id, comment, rating):
            self.bot.reply_to(message, "Спасибо за ваш отзыв о галерее! 🌟")
        else:
            self.bot.reply_to(message, "Произошла ошибка при сохранении отзыва. Попробуйте позже.")
        
        # Очищаем состояние пользователя
        del self.user_states[user_id]

    def handle_text(self, message):
        """Обработка текстовых сообщений"""
        if message.text == "📚 Каталог художников":
            self.show_artists(message)
        elif message.text == "🖼 Каталог картин":
            self.show_paintings(message)
        elif message.text == "🔍 Найти картину по фото":
            self.bot.reply_to(message, "Пожалуйста, отправьте фотографию картины.")
        elif message.text == "📝 Отзывы о галерее":
            self.show_gallery_reviews(message)
        elif message.text == "❓ Помощь":
            self.help_command(message)
        else:
            # Проверяем состояние пользователя
            user_id = message.from_user.id
            if user_id in self.user_states:
                state = self.user_states[user_id]['state']
                if state == 'waiting_comment':
                    self.handle_review_text(message)
                elif state == 'waiting_gallery_comment':
                    self.handle_gallery_review_text(message)
                elif state == 'waiting_artist_name':
                    self.handle_artist_name(message)
                elif state == 'waiting_artist_biography':
                    self.handle_artist_biography(message)
                elif state == 'waiting_artist_style':
                    self.handle_artist_style(message)
                elif state == 'waiting_painting_title':
                    self.handle_painting_title(message)
                elif state == 'waiting_painting_description':
                    self.handle_painting_description(message)
                elif state == 'waiting_painting_year':
                    self.handle_painting_year(message)
                elif state == 'waiting_review_id':
                    self.handle_review_deletion(message)
                elif state == 'waiting_edit_painting_title':
                    self.handle_edit_painting_title(message)
                elif state == 'waiting_edit_painting_description':
                    self.handle_edit_painting_description(message)
                elif state == 'waiting_edit_painting_year':
                    self.handle_edit_painting_year(message)
                elif state.startswith('waiting_edit_artist_'):
                    self.handle_edit_artist_text(message)

    def handle_artist_name(self, message):
        """Обработка ввода имени художника"""
        user_id = message.from_user.id
        self.user_states[user_id]['artist_name'] = message.text
        self.user_states[user_id]['state'] = 'waiting_artist_biography'
        self.bot.reply_to(message, "Введите биографию художника:")

    def handle_artist_biography(self, message):
        """Обработка ввода биографии художника"""
        user_id = message.from_user.id
        self.user_states[user_id]['artist_biography'] = message.text
        self.user_states[user_id]['state'] = 'waiting_artist_style'
        self.bot.reply_to(message, "Введите стиль художника:")

    def handle_artist_style(self, message):
        """Обработка ввода стиля художника"""
        user_id = message.from_user.id
        artist_data = {
            'name': self.user_states[user_id]['artist_name'],
            'biography': self.user_states[user_id]['artist_biography'],
            'style': message.text
        }
        
        if self.db.add_artist(artist_data):
            self.bot.reply_to(message, "Художник успешно добавлен! 🎨")
        else:
            self.bot.reply_to(message, "Произошла ошибка при добавлении художника.")
        
        del self.user_states[user_id]

    def handle_painting_title(self, message):
        """Обработка ввода названия картины"""
        user_id = message.from_user.id
        if user_id not in self.user_states:
            return

        # Если пользователь добавляет новую картину
        if self.user_states[user_id].get('state') == 'waiting_painting_title':
            self.user_states[user_id]['painting_data'] = {
                'title': message.text
            }
            self.user_states[user_id]['state'] = 'waiting_painting_description'
            self.bot.reply_to(message, "Введите описание картины:")
        else:
            # Если редактирование
            try:
                painting_id = self.user_states[user_id]['painting_id']
                new_title = message.text

                if self.db.edit_painting(painting_id, 'title', new_title):
                    self.bot.reply_to(message, "Название картины успешно обновлено! 🎨")
                else:
                    self.bot.reply_to(message, "Произошла ошибка при обновлении названия.")
            except Exception as e:
                self.bot.reply_to(message, "Произошла ошибка при обновлении названия.")
            finally:
                del self.user_states[user_id]

    def handle_painting_description(self, message):
        """Обработка ввода описания картины"""
        user_id = message.from_user.id
        if user_id not in self.user_states:
            return

        # Если пользователь добавляет новую картину
        if self.user_states[user_id].get('state') == 'waiting_painting_description':
            self.user_states[user_id]['painting_data']['description'] = message.text
            self.user_states[user_id]['state'] = 'waiting_painting_year'
            self.bot.reply_to(message, "Введите год создания картины:")
        else:
            try:
                painting_id = self.user_states[user_id]['painting_id']
                new_description = message.text
                if self.db.edit_painting(painting_id, 'description', new_description):
                    self.bot.reply_to(message, "Описание картины успешно обновлено! 🎨")
                else:
                    self.bot.reply_to(message, "Произошла ошибка при обновлении описания.")
            except Exception as e:
                self.bot.reply_to(message, "Произошла ошибка при обновлении описания.")
            finally:
                del self.user_states[user_id]

    def handle_painting_year(self, message):
        """Обработка ввода года создания картины"""
        user_id = message.from_user.id
        if user_id not in self.user_states:
            return

        # Если пользователь добавляет новую картину
        if self.user_states[user_id].get('state') == 'waiting_painting_year':
            try:
                new_year = int(message.text)
                self.user_states[user_id]['painting_data']['year'] = new_year
                self.user_states[user_id]['state'] = 'waiting_painting_image'
                self.bot.reply_to(message, "Пожалуйста, отправьте изображение картины.")
            except ValueError:
                self.bot.reply_to(message, "Пожалуйста, введите корректный год.")
                return
        else:
            try:
                new_year = int(message.text)
                painting_id = self.user_states[user_id]['painting_id']
                if self.db.edit_painting(painting_id, 'year', new_year):
                    self.bot.reply_to(message, "Год создания картины успешно обновлен! 🎨")
                else:
                    self.bot.reply_to(message, "Произошла ошибка при обновлении года.")
            except ValueError:
                self.bot.reply_to(message, "Пожалуйста, введите корректный год.")
                return
            except Exception as e:
                self.bot.reply_to(message, "Произошла ошибка при обновлении года.")
            finally:
                del self.user_states[user_id]

    def handle_painting_image(self, message):
        """Обработка загрузки изображения картины"""
        user_id = message.from_user.id
        if not message.photo:
            self.bot.reply_to(message, "Пожалуйста, отправьте изображение.")
            return
        
        try:
            # Получаем файл изображения
            file_info = self.bot.get_file(message.photo[-1].file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            
            # Создаем директорию, если она не существует
            os.makedirs("images", exist_ok=True)
            
            # Сохраняем изображение
            image_path = f"{self.user_states[user_id]['painting_data']['title']}.jpg"
            with open(image_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            # Добавляем путь к изображению в данные картины
            self.user_states[user_id]['painting_data']['image_path'] = image_path
            
            # Сохраняем картину в базу
            if self.db.add_painting(self.user_states[user_id]['painting_data']):
                self.bot.reply_to(message, "Картина успешно добавлена! 🖼")
            else:
                self.bot.reply_to(message, "Произошла ошибка при добавлении картины.")
            
            # Очищаем состояние пользователя
            del self.user_states[user_id]
            
        except ConnectionError as e:
            self.bot.reply_to(message, "Произошла ошибка подключения. Пожалуйста, попробуйте еще раз.")
        except Exception as e:
            self.bot.reply_to(message, "Произошла ошибка при обработке изображения. Попробуйте еще раз.")
            return

    def handle_review_deletion(self, message):
        """Обработка удаления отзыва"""
        try:
            review_id = int(message.text)
            if self.db.delete_review(review_id):
                self.bot.reply_to(message, "Отзыв успешно удален!")
            else:
                self.bot.reply_to(message, "Отзыв не найден.")
        except ValueError:
            self.bot.reply_to(message, "Пожалуйста, введите корректный ID отзыва.")
        
        del self.user_states[message.from_user.id]

    def handle_edit_artist_callback(self, call):
        """Обработка выбора художника для редактирования"""
        data_parts = call.data.split('_')
        
        if len(data_parts) == 3:  # edit_artist_1
            artist_id = int(data_parts[2])
            artist = self.db.get_artist(artist_id)
            
            markup = types.InlineKeyboardMarkup()
            buttons = [
                types.InlineKeyboardButton("Изменить имя", callback_data=f"edit_artist_name_{artist_id}"),
                types.InlineKeyboardButton("Изменить биографию", callback_data=f"edit_artist_bio_{artist_id}"),
                types.InlineKeyboardButton("Изменить стиль", callback_data=f"edit_artist_style_{artist_id}")
            ]
            markup.add(*buttons)
            
            self.bot.edit_message_text(
                f"Выберите, что хотите изменить:\n\n"
                f"Имя: {artist['name']}\n"
                f"Биография: {artist['biography']}\n"
                f"Стиль: {artist['style']}",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
        elif len(data_parts) == 4:  # edit_artist_name_1, edit_artist_bio_1, edit_artist_style_1
            field_type = data_parts[2]  # name, bio, style
            artist_id = int(data_parts[3])
            
            # Сохраняем состояние пользователя
            self.user_states[call.from_user.id] = {
                'state': f'waiting_edit_artist_{field_type}',
                'artist_id': artist_id
            }
            
            field_names = {
                'name': 'имя',
                'bio': 'биографию',
                'style': 'стиль'
            }
            
            self.bot.edit_message_text(
                f"Введите новое {field_names[field_type]} художника:",
                call.message.chat.id,
                call.message.message_id
            )

    def handle_edit_artist_text(self, message):
        """Обработка ввода нового значения для редактирования художника"""
        user_id = message.from_user.id
        if user_id not in self.user_states:
            return
        
        state = self.user_states[user_id]['state']
        artist_id = self.user_states[user_id]['artist_id']
        
        field_mapping = {
            'waiting_edit_artist_name': 'name',
            'waiting_edit_artist_bio': 'biography',
            'waiting_edit_artist_style': 'style'
        }
        
        field = field_mapping.get(state)
        if not field:
            return
        
        if self.db.edit_artist(artist_id, field, message.text):
            self.bot.reply_to(message, "Информация о художнике успешно обновлена! 🎨")
        else:
            self.bot.reply_to(message, "Произошла ошибка при обновлении информации.")
        
        del self.user_states[user_id]

    def handle_delete_artist_callback(self, call):
        """Обработка удаления художника"""
        artist_id = int(call.data.split('_')[2])
        if self.db.delete_artist(artist_id):
            self.bot.answer_callback_query(call.id, "Художник успешно удален!")
            self.bot.edit_message_text(
                "Художник успешно удален!",
                call.message.chat.id,
                call.message.message_id
            )
        else:
            self.bot.answer_callback_query(call.id, "Ошибка при удалении художника.")

    def handle_edit_painting_title(self, message):
        """Обработка ввода нового названия картины"""
        user_id = message.from_user.id
        if user_id not in self.user_states:
            return
        
        try:
            painting_id = self.user_states[user_id]['painting_id']
            new_title = message.text
            
            if self.db.edit_painting(painting_id, 'title', new_title):
                self.bot.reply_to(message, "Название картины успешно обновлено! 🎨")
            else:
                self.bot.reply_to(message, "Произошла ошибка при обновлении названия.")
        except Exception as e:
            self.bot.reply_to(message, "Произошла ошибка при обновлении названия.")
        finally:
            del self.user_states[user_id]

    def handle_edit_painting_description(self, message):
        """Обработка ввода нового описания картины"""
        user_id = message.from_user.id
        if user_id not in self.user_states:
            return
        
        try:
            painting_id = self.user_states[user_id]['painting_id']
            new_description = message.text
            
            if self.db.edit_painting(painting_id, 'description', new_description):
                self.bot.reply_to(message, "Описание картины успешно обновлено! 🎨")
            else:
                self.bot.reply_to(message, "Произошла ошибка при обновлении описания.")
        except Exception as e:
            self.bot.reply_to(message, "Произошла ошибка при обновлении описания.")
        finally:
            del self.user_states[user_id]

    def handle_edit_painting_year(self, message):
        """Обработка ввода нового года создания картины"""
        user_id = message.from_user.id
        if user_id not in self.user_states:
            return
        
        try:
            new_year = int(message.text)
            painting_id = self.user_states[user_id]['painting_id']
            
            if self.db.edit_painting(painting_id, 'year', new_year):
                self.bot.reply_to(message, "Год создания картины успешно обновлен! 🎨")
            else:
                self.bot.reply_to(message, "Произошла ошибка при обновлении года.")
        except ValueError:
            self.bot.reply_to(message, "Пожалуйста, введите корректный год.")
            return
        except Exception as e:
            self.bot.reply_to(message, "Произошла ошибка при обновлении года.")
        finally:
            del self.user_states[user_id] 

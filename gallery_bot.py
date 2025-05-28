import telebot
from config import BOT_TOKEN
from handlers import Handlers
from telebot import types
import time
from requests.exceptions import ConnectionError, ReadTimeout
import pandas as pd
from detect import run

bot = telebot.TeleBot(BOT_TOKEN)
handlers = Handlers(bot)

def safe_send_message(chat_id, text, **kwargs):
    """Безопасная отправка сообщения с повторными попытками"""
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            return bot.send_message(chat_id, text, **kwargs)
        except (ConnectionError, ReadTimeout) as e:
            if attempt == max_retries - 1:
                print(f"Failed to send message after {max_retries} attempts: {e}")
                raise
            print(f"Connection error, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2

@bot.message_handler(commands=['start'])
def start(message):
    try:
        handlers.start(message)
    except Exception as e:
        print(f"Error in start command: {e}")
        safe_send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

@bot.message_handler(commands=['help'])
def help_command(message):
    handlers.help_command(message)

@bot.message_handler(commands=['yanGPT'])
def start_yanGPT(message):
    """Обработчик команды /yanGPT"""
   bot.reply_to(message, 
        "Привет! Ты можешь:\n"
        "1. Написать описание картины — я угадаю её название и автора. Обязательно используй слово 'описание'\n"
        "2. Просто поболтать со мной.\n\n"
        "Попробуй! Например: 'описание: Русский витязь перед камнем с предупреждением'"
    )
    self.user_states[user_id]['state'] = 'in_converation'

@bot.message_handler(commands=['request_role'])
def request_role(message):
    handlers.request_role(message)

@bot.message_handler(commands=['add_test_reviews'])
def add_test_reviews(message):
    if handlers.db.get_user_role(message.from_user.id) == 'admin':
        if handlers.db.add_test_reviews():
            bot.reply_to(message, "Тестовые отзывы успешно добавлены!")
        else:
            bot.reply_to(message, "Произошла ошибка при добавлении отзывов.")
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['gallery_reviews'])
def gallery_reviews(message):
    handlers.show_gallery_reviews(message)

@bot.message_handler(commands=['add_gallery_review'])
def add_gallery_review(message):
    markup = types.InlineKeyboardMarkup()
    for rating in range(1, 6):
        button = types.InlineKeyboardButton(
            text=f"{'⭐' * rating}",
            callback_data=f"gallery_rating_{rating}"
        )
        markup.add(button)
    
    handlers.user_states[message.from_user.id] = {
        'state': 'waiting_gallery_review'
    }
    
    bot.reply_to(message, "Оцените галерею от 1 до 5 звезд:", reply_markup=markup)

@bot.message_handler(commands=['add_artist'])
def add_artist(message):
    if handlers.db.get_user_role(message.from_user.id) in ['admin', 'curator']:
        handlers.user_states[message.from_user.id] = {
            'state': 'waiting_artist_name'
        }
        bot.reply_to(message, "Введите имя художника:")
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['edit_artist'])
def edit_artist(message):
    if handlers.db.get_user_role(message.from_user.id) in ['admin', 'curator']:
        artists = handlers.db.get_artists()
        if artists.empty:
            bot.reply_to(message, "В базе нет художников для редактирования.")
            return
        
        markup = types.InlineKeyboardMarkup()
        for _, artist in artists.iterrows():
            button = types.InlineKeyboardButton(
                text=f"🎨 {artist['name']}",
                callback_data=f"edit_artist_{artist['id']}"
            )
            markup.add(button)
        
        bot.reply_to(message, "Выберите художника для редактирования:", reply_markup=markup)
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['delete_artist'])
def delete_artist(message):
    if handlers.db.get_user_role(message.from_user.id) in ['admin', 'curator']:
        artists = handlers.db.get_artists()
        if artists.empty:
            bot.reply_to(message, "В базе нет художников для удаления.")
            return
        
        markup = types.InlineKeyboardMarkup()
        for _, artist in artists.iterrows():
            button = types.InlineKeyboardButton(
                text=f"🎨 {artist['name']}",
                callback_data=f"delete_artist_{artist['id']}"
            )
            markup.add(button)
        
        bot.reply_to(message, "Выберите художника для удаления:", reply_markup=markup)
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['add_painting'])
def add_painting(message):
    try:
        if handlers.db.get_user_role(message.from_user.id) in ['admin', 'curator']:
            artists = handlers.db.get_artists()
            if artists.empty:
                safe_send_message(message.chat.id, "Сначала добавьте хотя бы одного художника.")
                return
            
            markup = types.InlineKeyboardMarkup()
            for _, artist in artists.iterrows():
                button = types.InlineKeyboardButton(
                    text=f"🎨 {artist['name']}",
                    callback_data=f"add_painting_artist_{artist['id']}"
                )
                markup.add(button)
            
            safe_send_message(
                message.chat.id,
                "Выберите художника для новой картины:",
                reply_markup=markup
            )
        else:
            safe_send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
    except Exception as e:
        print(f"Error in add_painting command: {e}")
        safe_send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

@bot.message_handler(commands=['delete_review'])
def delete_review(message):
    if handlers.db.get_user_role(message.from_user.id) in ['admin', 'curator']:
        handlers.user_states[message.from_user.id] = {
            'state': 'waiting_review_id'
        }
        bot.reply_to(message, "Введите ID отзыва для удаления:")
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")

@bot.message_handler(commands=['delete_painting'])
def delete_painting(message):
    try:
        if handlers.db.get_user_role(message.from_user.id) in ['admin', 'curator']:
            paintings = handlers.db.get_paintings()
            if paintings.empty:
                safe_send_message(message.chat.id, "В базе нет картин для удаления.")
                return
            
            markup = types.InlineKeyboardMarkup()
            for _, painting in paintings.iterrows():
                button = types.InlineKeyboardButton(
                    text=f"🖼 {painting['title']}",
                    callback_data=f"delete_painting_{painting['id']}"
                )
                markup.add(button)
            
            safe_send_message(
                message.chat.id,
                "Выберите картину для удаления:",
                reply_markup=markup
            )
        else:
            safe_send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
    except Exception as e:
        print(f"Error in delete_painting command: {e}")
        safe_send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

@bot.message_handler(commands=['delete_gallery_review'])
def delete_gallery_review(message):
    try:
        if handlers.db.get_user_role(message.from_user.id) in ['admin', 'curator']:
            reviews, _ = handlers.db.get_gallery_reviews()
            if reviews.empty:
                safe_send_message(message.chat.id, "Нет отзывов о галерее для удаления.")
                return
            
            markup = types.InlineKeyboardMarkup()
            for _, review in reviews.iterrows():
                button = types.InlineKeyboardButton(
                    text=f"⭐️ {review['rating']} - {review['text'][:30]}...",
                    callback_data=f"delete_gallery_review_{review['id']}"
                )
                markup.add(button)
            
            safe_send_message(
                message.chat.id,
                "Выберите отзыв для удаления:",
                reply_markup=markup
            )
        else:
            safe_send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
    except Exception as e:
        print(f"Error in delete_gallery_review command: {e}")
        safe_send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

@bot.message_handler(commands=['edit_painting'])
def edit_painting(message):
    try:
        if handlers.db.get_user_role(message.from_user.id) in ['admin', 'curator']:
            paintings = handlers.db.get_paintings()
            if paintings.empty:
                safe_send_message(message.chat.id, "В базе нет картин для редактирования.")
                return
            
            markup = types.InlineKeyboardMarkup()
            for _, painting in paintings.iterrows():
                button = types.InlineKeyboardButton(
                    text=f"🖼 {painting['title']}",
                    callback_data=f"edit_painting_{painting['id']}"
                )
                markup.add(button)
            
            safe_send_message(
                message.chat.id,
                "Выберите картину для редактирования:",
                reply_markup=markup
            )
        else:
            safe_send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
    except Exception as e:
        print(f"Error in edit_painting command: {e}")
        safe_send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "📚 Каталог художников":
        handlers.show_artists(message)
    elif message.text == "🖼 Каталог картин":
        handlers.show_paintings(message)
    elif message.text == "🔍 Найти картину по фото":
        bot.reply_to(message, "Пожалуйста, отправьте фотографию картины.")
    elif message.text == "📝 Отзывы о галерее":
        handlers.show_gallery_reviews(message)
    elif message.text == "❓ Помощь":
        handlers.help_command(message)
    else:
        user_id = message.from_user.id
        if user_id in handlers.user_states:
            state = handlers.user_states[user_id]['state']
            print(f"Processing state: {state}")
            
            if state == 'waiting_comment':
                handlers.handle_review_text(message)
            elif state == 'waiting_gallery_comment':
                handlers.handle_gallery_review_text(message)
            elif state == 'in_conversation':
                handlers.handle_message(message)
            elif state == 'waiting_artist_name':
                handlers.handle_artist_name(message)
            elif state == 'waiting_artist_biography':
                handlers.handle_artist_biography(message)
            elif state == 'waiting_artist_style':
                handlers.handle_artist_style(message)
            elif state == 'waiting_painting_title':
                handlers.handle_painting_title(message)
            elif state == 'waiting_painting_description':
                handlers.handle_painting_description(message)
            elif state == 'waiting_painting_year':
                handlers.handle_painting_year(message)
            elif state == 'waiting_review_id':
                handlers.handle_review_deletion(message)
            elif state == 'waiting_edit_painting_title':
                handlers.handle_edit_painting_title(message)
            elif state == 'waiting_edit_painting_description':
                handlers.handle_edit_painting_description(message)
            elif state == 'waiting_edit_painting_year':
                handlers.handle_edit_painting_year(message)
            elif state.startswith('waiting_edit_artist_'):
                handlers.handle_edit_artist_text(message)
            else:
                print(f"Unknown state: {state}")
                bot.reply_to(message, "Неизвестное состояние. Пожалуйста, начните сначала.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    if user_id in handlers.user_states and handlers.user_states[user_id]['state'] == 'waiting_painting_image':
        if 'artist_id' not in handlers.user_states[user_id]['painting_data']:
            artists = handlers.db.get_artists()
            if not artists.empty:
                handlers.user_states[user_id]['painting_data']['artist_id'] = int(artists.iloc[0]['id'])
            else:
                safe_send_message(message.chat.id, "Сначала добавьте хотя бы одного художника!")
                return
        handlers.handle_painting_image(message)
    else:
        handlers.handle_photo(message)

@bot.message_handler(content_types=['document'])
def handle_recognition(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg","wb") as f:
        f.write(downloaded_file)
    p_id = run(source="image.jpg")

    if(p_id is None):
        bot.reply_to(message,"Не удалось распознать картину")
        return
    p_db = pd.read_excel("data/paintings.xlsx")
    a_db = pd.read_excel("data/artists.xlsx")

    p_row = p_db[p_db['id'] == p_id].iloc[0]
    a_row = a_db[a_db['id'] == p_row['artist_id']].iloc[0]

    result = f"\"{p_row['title']}\" - {a_row['name']}, {p_row['year']}\n\n{p_row['description']}"
    bot.reply_to(message,result)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        if call.data == 'paintings':
            handlers.show_paintings(call.message)
        elif call.data.startswith('paintings_page_'):
            page = int(call.data.split('_')[2])
            handlers.show_paintings(call, page)
        elif call.data.startswith('artists_page_'):
            page = int(call.data.split('_')[2])
            handlers.show_artists(call, page)
        elif call.data.startswith('painting_'):
            handlers.show_painting_details(call)
        elif call.data.startswith('artist_'):
            if call.data.startswith('artist_paintings_'):
                handlers.show_artist_paintings(call)
            else:
                handlers.show_artist_details(call)
        elif call.data.startswith('review_'):
            handlers.handle_review_callback(call)
        elif call.data.startswith('rating_'):
            handlers.handle_rating_callback(call)
        elif call.data.startswith('gallery_reviews_'):
            page = int(call.data.split('_')[2])
            handlers.show_gallery_reviews(call, page)
        elif call.data == 'add_gallery_review':
            handlers.handle_gallery_review_callback(call)
        elif call.data.startswith('gallery_rating_'):
            handlers.handle_gallery_rating_callback(call)
        elif call.data.startswith('edit_artist_'):
            if handlers.db.get_user_role(call.from_user.id) in ['admin', 'curator']:
                handlers.handle_edit_artist_callback(call)
            else:
                bot.answer_callback_query(call.id, "У вас нет прав для выполнения этой команды.")
        elif call.data.startswith('delete_artist_'):
            if handlers.db.get_user_role(call.from_user.id) in ['admin', 'curator']:
                handlers.handle_delete_artist_callback(call)
            else:
                bot.answer_callback_query(call.id, "У вас нет прав для выполнения этой команды.")
        elif call.data.startswith('edit_painting_'):
            if handlers.db.get_user_role(call.from_user.id) in ['admin', 'curator']:
                data_parts = call.data.split('_')
                if len(data_parts) == 3:
                    try:
                        painting_id = int(data_parts[2])
                        painting = handlers.db.get_painting(painting_id)
                        
                        markup = types.InlineKeyboardMarkup()
                        buttons = [
                            types.InlineKeyboardButton("Изменить название", callback_data=f"edit_painting_title_{painting_id}"),
                            types.InlineKeyboardButton("Изменить описание", callback_data=f"edit_painting_description_{painting_id}"),
                            types.InlineKeyboardButton("Изменить год", callback_data=f"edit_painting_year_{painting_id}")
                        ]
                        markup.add(*buttons)
                        
                        bot.edit_message_text(
                            f"Выберите, что хотите изменить:\n\n"
                            f"Название: {painting['title']}\n"
                            f"Описание: {painting['description']}\n"
                            f"Год: {painting['year']}",
                            call.message.chat.id,
                            call.message.message_id,
                            reply_markup=markup
                        )
                    except ValueError:
                        bot.answer_callback_query(call.id, "Ошибка: неверный ID картины")
                elif len(data_parts) == 4:
                    field_type = data_parts[2]
                    try:
                        painting_id = int(data_parts[3])
                        
                        handlers.user_states[call.from_user.id] = {
                            'state': f'waiting_edit_painting_{field_type}',
                            'painting_id': painting_id
                        }
                        
                        field_names = {
                            'title': 'название',
                            'description': 'описание',
                            'year': 'год создания'
                        }
                        
                        bot.edit_message_text(
                            f"Введите новое {field_names[field_type]} картины:",
                            call.message.chat.id,
                            call.message.message_id
                        )
                    except ValueError:
                        bot.answer_callback_query(call.id, "Ошибка: неверный ID картины")
            else:
                bot.answer_callback_query(call.id, "У вас нет прав для выполнения этой команды.")
        elif call.data.startswith('delete_painting_'):
            if handlers.db.get_user_role(call.from_user.id) in ['admin', 'curator']:
                try:
                    painting_id = int(call.data.split('_')[2])
                    if handlers.db.delete_painting(painting_id):
                        bot.answer_callback_query(call.id, "Картина успешно удалена!")
                        bot.edit_message_text(
                            "Картина успешно удалена!",
                            call.message.chat.id,
                            call.message.message_id
                        )
                    else:
                        bot.answer_callback_query(call.id, "Ошибка при удалении картины.")
                except ValueError:
                    bot.answer_callback_query(call.id, "Ошибка: неверный ID картины")
            else:
                bot.answer_callback_query(call.id, "У вас нет прав для выполнения этой команды.")
        elif call.data.startswith('delete_gallery_review_'):
            if handlers.db.get_user_role(call.from_user.id) in ['admin', 'curator']:
                try:
                    review_id = int(call.data.split('_')[3])
                    if handlers.db.delete_gallery_review(review_id):
                        bot.answer_callback_query(call.id, "Отзыв успешно удален!")
                        bot.edit_message_text(
                            "Отзыв успешно удален!",
                            call.message.chat.id,
                            call.message.message_id
                        )
                    else:
                        bot.answer_callback_query(call.id, "Ошибка при удалении отзыва.")
                except ValueError:
                    bot.answer_callback_query(call.id, "Ошибка: неверный ID отзыва")
            else:
                bot.answer_callback_query(call.id, "У вас нет прав для выполнения этой команды.")
        elif call.data.startswith('add_painting_artist_'):
            if handlers.db.get_user_role(call.from_user.id) in ['admin', 'curator']:
                try:
                    artist_id = int(call.data.split('_')[3])
                    handlers.user_states[call.from_user.id] = {
                        'state': 'waiting_painting_title',
                        'artist_id': artist_id
                    }
                    bot.edit_message_text(
                        "Введите название картины:",
                        call.message.chat.id,
                        call.message.message_id
                    )
                except ValueError:
                    bot.answer_callback_query(call.id, "Ошибка: неверный ID художника")
            else:
                bot.answer_callback_query(call.id, "У вас нет прав для выполнения этой команды.")
        elif call.data.startswith('qr_'):
            handlers.handle_qr_callback(call)
    except Exception as e:
        print(f"Error in callback handler: {e}")
        bot.answer_callback_query(call.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

if __name__ == '__main__':
    print("Бот запущен...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"Error in polling: {e}")
            time.sleep(15)

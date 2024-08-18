from telebot.types import Message, CallbackQuery
from telebot import types
from api_kinopoisk.core import api_kp
from api_telegramm_bot.core import bot
from api_telegramm_bot.keyboards.inline.inline import markup_genres
from api_telegramm_bot.utils.utils import is_number
from api_telegramm_bot.resource.path import DEFAULT_IMAGE_PATH
from api_telegramm_bot.config.config import MAX_VIEW_FILMS
from api_telegramm_bot.utils.utils import search_films

low_params = {
    "genre": "",
    "count": 0
}


@bot.message_handler(commands=['low'])
def low(message: Message) -> None:
    global low_params
    low_params = {
        "genre": "",
        "count": 0
    }
    bot.send_message(message.chat.id, "Выберите жанр фильмов для поиска:", reply_markup=markup_genres("low"))


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('low_genre_'))
def get_low_genres_callback(callback: CallbackQuery) -> None:
    global low_params
    genre = callback.data[10:]
    low_params["genre"] = genre
    msg = bot.send_message(callback.message.chat.id, f"Введите кол-во фильмов для поиска (0-{MAX_VIEW_FILMS}):")
    bot.register_next_step_handler(msg, low_output_films)


def low_output_films(message):
    global low_params
    chat_id = message.chat.id
    msg_text = message.text
    count = is_number(msg_text)
    if count is None or count < 0 or count > MAX_VIEW_FILMS:
        low_params["count"] = 0
        msg = bot.send_message(chat_id, f"Неверный ввод - должно быть число от 0 до {MAX_VIEW_FILMS}. "
                                        f"Введите значение заново:")
        bot.register_next_step_handler(msg, low_output_films)
    else:
        low_params["count"] = count
        bot.send_message(chat_id, f"Результаты поиска: ")
        films = search_films(genre=low_params["genre"], limit=low_params["count"])
        for film in films:
            bot.send_photo(chat_id, photo=film[0], caption=film[1])
        low_params = {
            "genre": "",
            "count": 0
        }

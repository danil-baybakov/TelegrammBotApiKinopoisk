from telebot.types import Message, CallbackQuery
from telebot import types
from api_kinopoisk.core import api_kp
from api_telegramm_bot.core import bot
from api_telegramm_bot.keyboards.inline.inline import markup_genres
from api_telegramm_bot.utils.utils import is_number, is_float
from api_telegramm_bot.resource.path import DEFAULT_IMAGE_PATH
from api_telegramm_bot.config.config import MAX_VIEW_FILMS
from api_telegramm_bot.utils.utils import search_films

custom_params = {
    "genre": "",
    "min_rating": 0.0,
    "max_rating": 10.0,
    "count": 0
}


@bot.message_handler(commands=['custom'])
def low(message: Message) -> None:
    global custom_params
    custom_params = {
        "genre": "",
        "count": 0
    }
    bot.send_message(message.chat.id, "Выберите жанр фильмов для поиска:", reply_markup=markup_genres("custom"))


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('custom_genre_'))
def get_low_genres_callback(callback: CallbackQuery) -> None:
    global custom_params
    genre = callback.data[13:]
    custom_params["genre"] = genre
    msg = bot.send_message(callback.message.chat.id, f"Введите кол-во фильмов для поиска (0-{MAX_VIEW_FILMS}):")
    bot.register_next_step_handler(msg, custom_set_min_rating)


def custom_set_min_rating(message):
    chat_id = message.chat.id
    msg_text = message.text
    count = is_number(msg_text)
    if count is None or count < 0 or count > MAX_VIEW_FILMS:
        custom_params["count"] = 0
        msg = bot.send_message(chat_id, f"Неверный ввод - должно быть число от 0 до {MAX_VIEW_FILMS}. "
                                        f"Введите значение заново:")
        bot.register_next_step_handler(msg, custom_set_min_rating)
    else:
        custom_params["count"] = count
        msg = bot.send_message(message.chat.id, f"Введите минимальный рейтинг для поиска (0-10):")
        bot.register_next_step_handler(msg, custom_set_max_rating)


def custom_set_max_rating(message):
    global custom_params
    chat_id = message.chat.id
    msg_text = message.text
    min_rating = is_float(msg_text)
    if min_rating is None or min_rating < 0 or min_rating > 10:
        custom_params["min_rating"] = 0
        msg = bot.send_message(chat_id, f"Неверный ввод - должно быть число от 0 до 10. "
                                        f"Введите значение заново:")
        bot.register_next_step_handler(msg, custom_set_max_rating)
    else:
        custom_params["min_rating"] = min_rating
        msg = bot.send_message(message.chat.id, f"Введите максимальный рейтинг для поиска (0-10):")
        bot.register_next_step_handler(msg, custom_output_films)


def custom_output_films(message):
    global custom_params
    chat_id = message.chat.id
    msg_text = message.text
    max_rating = is_float(msg_text)
    if max_rating is None or max_rating < 0 or max_rating > 10:
        custom_params["max_rating"] = 0
        msg = bot.send_message(chat_id, f"Неверный ввод - должно быть число от 0 до 10. "
                                        f"Введите значение заново:")
        bot.register_next_step_handler(msg, custom_output_films)
    elif max_rating < custom_params["min_rating"]:
        custom_params["max_rating"] = 0
        msg = bot.send_message(chat_id, f"Максимальный рейтинг не может быть меньше минимального. "
                                        f"Введите значение заново:")
        bot.register_next_step_handler(msg, custom_output_films)
    else:
        custom_params["max_rating"] = max_rating
        bot.send_message(chat_id, f"Результаты поиска: ")
        films = search_films(
            genre=custom_params["genre"],
            limit=int(custom_params["count"]),
            rating_min=custom_params["min_rating"],
            rating_max=custom_params["max_rating"]
        )
        for film in films:
            bot.send_photo(chat_id, photo=film[0], caption=film[1])
        custom_params = {
            "genre": "",
            "min_rating": 0,
            "max_rating": 10.0,
            "count": 0.0
        }

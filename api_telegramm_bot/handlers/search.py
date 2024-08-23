from telebot.types import Message, CallbackQuery
from api_telegramm_bot.core import bot
from api_telegramm_bot.keyboards.inline.inline import markup_genres
from api_telegramm_bot.utils.utils import is_number, is_float
from api_telegramm_bot.config.config import MAX_VIEW_FILMS
from api_telegramm_bot.utils.utils import search_films
from api_database.core import api_db
from api_database.common.model import ParamsStorage, History


@bot.message_handler(commands=['low', 'high', 'custom'])
def search(message: Message) -> None:
    cmd = message.text
    cid = message.chat.id
    api_db.delete_param_storage_by_cid(model=ParamsStorage, cid=cid)
    api_db.set_param_storage_by_cid(
        model=ParamsStorage,
        cid=cid,
        command=cmd,
        order=-1 if cmd == "/high" else 1,
        min_rating=None if cmd == "/custom" else 0.0,
        max_rating=None if cmd == "/custom" else 10.0
    )
    bot.send_message(message.chat.id, "Выберите жанр фильмов для поиска:", reply_markup=markup_genres())


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('genre_'))
def get_genres_callback(callback: CallbackQuery) -> None:
    cid = callback.message.chat.id
    cmd = api_db.get_param_storage_by_cid(model=ParamsStorage, cid=cid).command
    genre = callback.data[6:]
    api_db.set_param_storage_by_cid(model=ParamsStorage, cid=cid, genre=genre)
    msg = bot.send_message(callback.message.chat.id, f"Введите кол-во фильмов для поиска (0-{MAX_VIEW_FILMS}):")
    bot.register_next_step_handler(msg, set_min_rating if cmd == "/custom" else output_films)


def set_min_rating(message):
    cid = message.chat.id
    msg_text = message.text
    limit = is_number(msg_text)
    if limit is None or limit < 0 or limit > MAX_VIEW_FILMS:
        msg = bot.send_message(cid, f"Неверный ввод - должно быть число от 0 до {MAX_VIEW_FILMS}. "
                                    f"Введите значение заново:")
        bot.register_next_step_handler(msg, set_min_rating)
    else:
        api_db.set_param_storage_by_cid(model=ParamsStorage, cid=cid, limit=limit)
        msg = bot.send_message(message.chat.id, f"Введите минимальный рейтинг для поиска (0-10):")
        bot.register_next_step_handler(msg, set_max_rating)


def set_max_rating(message):
    cid = message.chat.id
    msg_text = message.text
    min_rating = is_float(msg_text)
    if min_rating is None or min_rating < 0 or min_rating > 10:
        msg = bot.send_message(cid, f"Неверный ввод - должно быть число от 0 до 10. "
                                    f"Введите значение заново:")
        bot.register_next_step_handler(msg, set_max_rating)
    else:
        api_db.set_param_storage_by_cid(model=ParamsStorage, cid=cid, min_rating=min_rating)
        msg = bot.send_message(message.chat.id, f"Введите максимальный рейтинг для поиска (0-10):")
        bot.register_next_step_handler(msg, output_films)


def output_films(message):
    cid = message.chat.id
    cmd = api_db.get_param_storage_by_cid(model=ParamsStorage, cid=cid).command
    msg_text = message.text
    if cmd == "/custom":
        min_rating = api_db.get_param_storage_by_cid(model=ParamsStorage, cid=cid).min_rating
        max_rating = is_float(msg_text)
        if max_rating is None or max_rating < 0 or max_rating > 10:
            msg = bot.send_message(cid, f"Неверный ввод - должно быть число от 0 до 10. "
                                        f"Введите значение заново:")
            bot.register_next_step_handler(msg, output_films)
            return
        if max_rating < min_rating:
            msg = bot.send_message(cid, f"Максимальный рейтинг не может быть меньше минимального. "
                                        f"Введите значение заново:")
            bot.register_next_step_handler(msg, output_films)
            return
        api_db.set_param_storage_by_cid(model=ParamsStorage, cid=cid, max_rating=max_rating)
    else:
        limit = is_number(msg_text)
        if limit is None or limit < 0 or limit > MAX_VIEW_FILMS:
            msg = bot.send_message(cid, f"Неверный ввод - должно быть число от 0 до {MAX_VIEW_FILMS}. "
                                        f"Введите значение заново:")
            bot.register_next_step_handler(msg, output_films)
            return
        api_db.set_param_storage_by_cid(model=ParamsStorage, cid=cid, limit=limit)

    bot.send_message(cid, f"Результаты поиска: ")
    params = api_db.get_param_storage_by_cid(model=ParamsStorage, cid=cid)
    films = search_films(
        genre=params.genre,
        limit=params.limit,
        sort_param=params.order,
        rating_min=params.min_rating,
        rating_max=params.max_rating
    )
    for film in films:
        bot.send_photo(cid, photo=film[0], caption=film[1])
    api_db.set_param_storage_by_cid(
        model=History,
        cid=params.cid,
        command=params.command,
        genre=params.genre,
        limit=params.limit,
        order=params.order,
        min_rating=params.min_rating,
        max_rating=params.max_rating,
        timestamp=params.timestamp
    )
    api_db.delete_param_storage_by_cid(model=ParamsStorage, cid=cid)

from telebot.types import Message, CallbackQuery
from api_telegramm_bot.core import bot
from api_telegramm_bot.keyboards.inline.inline import markup_genres
from api_telegramm_bot.utils.utils import is_number, is_float
from api_telegramm_bot.config.config import MAX_VIEW_FILMS
from api_database.core import api_db
from api_database.common.model import ParamsStorage, History
from typing import BinaryIO
from api_telegramm_bot.resource.path import DEFAULT_IMAGE_PATH
from api_kinopoisk.core import api_kp


@bot.message_handler(commands=['low', 'high', 'custom'])
def search(message: Message) -> None:
    """
    Функция обработчика команд /low, /high, /custom
    для поиска фильмов по заданным параметрам

    :param message: Объект сообщения
    """
    cmd = message.text  # команда
    cid = message.chat.id  # id чата
    # если в таблице БД хранения текущих параметров запроса
    # хранится запись с текущим cid удаляем ее
    api_db.delete_param_storage_by_cid(cid=cid)
    # и создаем новую
    api_db.set_param_storage_by_cid(
        model=ParamsStorage,
        cid=cid,
        command=cmd,
        order=-1 if cmd == "/high" else 1,
        min_rating=None if cmd == "/custom" else 0.0,
        max_rating=None if cmd == "/custom" else 10.0
    )
    # выводим клавиатуру выбора жанра для поиска фильмов
    bot.send_message(message.chat.id, "Выберите жанр фильмов для поиска:", reply_markup=markup_genres())


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('genre_'))
def get_genres_callback(callback: CallbackQuery) -> None:
    """
    Функция обработчика коллбэка выбора жанра фильма

    :param callback: Объект входящего запроса на каллбэк вызов с помощью каллбек-кнопки клавиатуры
    """
    cid = callback.message.chat.id  # id чата
    # из данных коллбека получаем текущий выбранный жанр
    genre = callback.data[6:]
    # сохраняем в таблицу БД хранения текущих параметров запроса полученный жанр
    api_db.set_param_storage_by_cid(model=ParamsStorage, cid=cid, genre=genre)
    # выводим сообщение c предложением ввода кол-ва фильмов для поиска
    msg = bot.send_message(callback.message.chat.id, f"Введите кол-во фильмов для поиска (1-{MAX_VIEW_FILMS}):")
    # после ответа пользователя вызываем коллбэк функцию
    # обработки ввода кол-ва фильмов для поиска
    bot.register_next_step_handler(msg, set_limit)


def set_limit(message: Message) -> None:
    """
    Коллбэк функция обработки ввода кол-ва фильмов для поиска

    :param message: Объект сообщения
    """
    cid = message.chat.id  # id чата
    msg_text = message.text  # текст сообщения

    # из таблицы БД хранения текущих параметров запроса получаем текущую команду
    cmd = api_db.get_param_storage_by_cid(cid=cid).command

    # валидируем ввод пользователя
    limit = is_number(msg_text)
    # если введенное число меньше 1 или больше программно установленного максимума
    # выводим сообщением о том что совершен некорректный ввод и повторяем ввод заново
    if limit is None or limit < 1 or limit > MAX_VIEW_FILMS:
        msg = bot.send_message(cid, f"Неверный ввод - должно быть число от 1 до {MAX_VIEW_FILMS}. "
                                    f"Введите значение заново:")
        bot.register_next_step_handler(msg, set_limit)
        return

    # сохраняем в таблицу БД хранения текущих параметров запроса кол-во фильмов для поиска
    api_db.set_param_storage_by_cid(model=ParamsStorage, cid=cid, limit=limit)
    # если команда "/custom" вызываем коллбэк функцию для обработки
    # ввода минимального рейтинга
    if cmd == "/custom":
        msg = bot.send_message(message.chat.id, f"Введите минимальный рейтинг для поиска (0-10):")
        bot.register_next_step_handler(msg, set_min_rating)
        return
    # иначе
    # вызываем функцию вывода списка фильмов
    output_films(message)


def set_min_rating(message: Message) -> None:
    """
    Коллбэк функция обработки ввода минимального рейтинга

    :param message: Объект сообщения
    """
    cid = message.chat.id  # id чата
    msg_text = message.text  # текст сообщения

    # валидируем ввод пользователя
    min_rating = is_float(msg_text)
    # если введенное число меньше 0 или больше 10
    # выводим сообщением о том что совершен некорректный ввод и повторяем ввод заново
    if min_rating is None or min_rating < 0 or min_rating > 10:
        msg = bot.send_message(cid, f"Неверный ввод - должно быть число от 0 до 10. "
                                    f"Введите значение заново:")
        bot.register_next_step_handler(msg, set_min_rating)
        return

    # сохраняем в таблицу БД хранения текущих параметров запроса минимальный рейтинг поиска фильмов
    api_db.set_param_storage_by_cid(model=ParamsStorage, cid=cid, min_rating=min_rating)

    # вызываем коллбэк функцию для обработки
    # ввода максимального рейтинга
    msg = bot.send_message(message.chat.id, f"Введите максимальный рейтинг для поиска (0-10):")
    bot.register_next_step_handler(msg, set_max_rating)


def set_max_rating(message: Message) -> None:
    """
    Коллбэк функция обработки ввода максимального рейтинга

    :param message: Объект сообщения
    """
    cid = message.chat.id  # id чата
    msg_text = message.text  # текст сообщения

    # из таблицы БД хранения текущих параметров запроса получаем текущий минимальный рейтинг поиска
    min_rating = api_db.get_param_storage_by_cid(cid=cid).min_rating

    # валидируем ввод пользователя
    max_rating = is_float(msg_text)
    # если введенное число меньше 0 или больше 10
    # выводим сообщением о том что совершен некорректный ввод и повторяем ввод заново
    if max_rating is None or max_rating < 0 or max_rating > 10:
        msg = bot.send_message(cid, f"Неверный ввод - должно быть число от 0 до 10. "
                                    f"Введите значение заново:")
        bot.register_next_step_handler(msg, set_max_rating)
        return
    # если введенный максимальный рейтинг меньше текущего заданного минимального
    # выводим сообщением о том что совершен некорректный ввод и повторяем ввод заново
    if max_rating < min_rating:
        msg = bot.send_message(cid, f"Максимальный рейтинг не может быть меньше минимального. "
                                    f"Введите значение заново:")
        bot.register_next_step_handler(msg, set_max_rating)
        return

    # сохраняем в таблицу БД хранения текущих параметров запроса максимальный рейтинг поиска фильмов
    api_db.set_param_storage_by_cid(model=ParamsStorage, cid=cid, max_rating=max_rating)

    # вызываем функцию вывода списка фильмов
    output_films(message)


def output_films(message: Message) -> None:
    """
    Функция вывода найденного списка фильмов

    :param message: Объект сообщения
    """
    cid = message.chat.id  # id чата

    # из БД получаем все параметры для поискового запроса фильмов
    params = api_db.get_param_storage_by_cid(cid=cid)

    # вызываем функцию вывода списка с данными для вывода в чат в виде карточек
    # с изображением постера и описанием
    films = search_films(
        genre=params.genre,
        limit=params.limit,
        sort_param=params.order,
        rating_min=params.min_rating,
        rating_max=params.max_rating
    )

    # в чат выводим список фильмов
    bot.send_message(cid, f"Результаты поиска: ")
    if films:
        for film in films:
            bot.send_photo(cid, photo=film[0], caption=film[1])
    else:
        bot.send_message(cid, "Фильмов по данному запросу не найдено... ")

    # сохраняем текущий запрос в БД в таблицу истории запросов
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

    # удаляем текущий запрос из таблицы БД для хранения текущих запросов
    api_db.delete_param_storage_by_cid( cid=cid)


def search_films(genre: str,
                 limit: int = 10,
                 sort_param: int = 1,
                 rating_min: float = 0.0,
                 rating_max: float = 10.0) -> list[tuple[BinaryIO | str, str]]:
    """
    Функция формирует список с данными для вывода в чат в виде карточек
    с изображением постера и описанием
    :param genre: жанр фильма
    :param limit: кол-во фильмов для вывода
    :param sort_param: тип сортировки: 1 - по возрастанию, -1 - по убыванию
    :param rating_min: минимальный рейтинг фильма
    :param rating_max: максимальный рейтинг фильма
    :return: список с данными фильмов поискового запроса
    :rtype: list[tuple[BinaryIO | str, str]]
    """
    # получаем из Api кинопоиска список с данными фильмов поискового запроса
    films = api_kp.get_films_by_filter(
        genre=genre,
        limit=limit,
        sort_param=sort_param,
        rating_min=rating_min,
        rating_max=rating_max)

    output = []

    # из полученного ответа от Api кинопоиска
    # формируем для каждого фильма карточку с изображением постера
    # и описанием
    list_films = films.get("docs", None)
    if list_films:
        for film in list_films:

            # постер
            poster = film.get("poster", None)
            url_preview = None
            if poster is not None:
                url_preview = poster.get("previewUrl", None)
                if url_preview is None:
                    url_preview = poster.get("url", None)
            if url_preview is None:
                url_preview = open(DEFAULT_IMAGE_PATH, "rb")

            # наименование
            name = film.get("name", None)
            if name is None:
                name = film.get("alternativeName", None)
                if name is None:
                    name = "***"

            # жанр
            genres = film.get("genres", None)
            if genres:
                genres = ', '.join([genre["name"] for genre in genres])
            else:
                genres = "***"

            # рейтинг
            rating = film.get("rating", None)
            if rating is not None:
                kp_rating = rating.get("kp", None)
                if kp_rating is None:
                    kp_rating = "***"
                imdb_rating = rating.get("imdb", None)
                if imdb_rating is None:
                    imdb_rating = "***"
            else:
                kp_rating, imdb_rating = "***", "***"

            # год выпуска
            year = film.get("year", None)
            if year is None:
                year = "***"

            # возрастное ограничение
            edge_rating = film.get("ageRating", None)
            if edge_rating is None:
                edge_rating = "***"
            else:
                edge_rating = f"{edge_rating}+"

            # описание
            description = film.get("description", None)
            if description is None:
                description = "__________"

            caption = (f"🌈Название: {name} \n🍿Жанр: {genres} \n☃️Кинопоиск: {kp_rating} \t 🦏IMDB: {imdb_rating} "
                       f"\n📅Год выпуска: {year} \n😯Возрастной рейтинг: {edge_rating} "
                       f"\n\n🎬Описание:\n{description}")

            output.append((url_preview, caption))
    return output

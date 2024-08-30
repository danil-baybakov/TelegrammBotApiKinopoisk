from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_kinopoisk.core import api_kp
from telebot.util import quick_markup


def markup_genres() -> InlineKeyboardMarkup:
    """
    Инлайн клавиатура выбора жанра для поиска фильмов
    """
    # из api Кинопоиска получаем полный список жанров для поиска
    genres = api_kp.get_list_genre_film()
    # создаем клавиатуру с коллбак кнопками
    # каждая кнопка соответствует определенному жанру
    buttons = {}
    for genre in genres:
        buttons[f'{genre["name"]}'] = {'callback_data': f'genre_{genre["name"]}'}
    markup = quick_markup(buttons, row_width=4)
    # возвращаем клавиатуру
    return markup


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_kinopoisk.core import api_kp
from telebot.util import quick_markup


def markup_genres() -> InlineKeyboardMarkup:
    genres = api_kp.get_list_genre_film()
    buttons = {}
    for genre in genres:
        buttons[f'{genre["name"]}'] = {'callback_data': f'{genre["name"]}'}
    markup = quick_markup(buttons, row_width=4)
    return markup


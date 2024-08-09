from telebot.types import Message, CallbackQuery
from telebot import types
from api_kinopoisk.core import api_kp
from api_telegramm_bot.core import bot
from api_telegramm_bot.keyboards.inline.inline import markup_genres


@bot.message_handler(commands=['low'])
def low(message: Message):
    bot.send_message(message.chat.id, "Выберите жанр фильмов для поиска: ", reply_markup=markup_genres())


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_genres(callback: CallbackQuery):
    if callback.data == "драма":
        bot.send_message(callback.message.chat.id, " Вы нажали на кнопку драма")

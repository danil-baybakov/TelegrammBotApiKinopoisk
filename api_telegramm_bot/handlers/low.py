from telebot.types import Message
from telebot import types

from api_telegramm_bot.core import bot


@bot.message_handler(commands=['low'])
def low(message: Message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Кнопка1")
    btn2 = types.InlineKeyboardButton("Кнопка1")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите жанр фильмов для поиска: ")

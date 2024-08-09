from telebot.types import Message, CallbackQuery

from api_telegramm_bot.core import bot
from telebot import types


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, message)
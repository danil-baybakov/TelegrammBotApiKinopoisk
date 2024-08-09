from telebot.types import Message, CallbackQuery

from api_telegramm_bot.core import bot
from telebot import types


@bot.message_handler(regexp=r'Привет')
@bot.message_handler(commands=['hello-world'])
def hello(message: Message):
    bot.send_message(message.chat.id, 'Привет')
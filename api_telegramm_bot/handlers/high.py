from telebot.types import Message

from api_telegramm_bot.core import bot


@bot.message_handler(commands=['high'])
def high(message: Message):
    bot.send_message(message.chat.id, 'high')

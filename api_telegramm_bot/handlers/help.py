from telebot.types import Message

from api_telegramm_bot.core import bot


@bot.message_handler(commands=['help'])
def help_(message: Message):
    bot.send_message(message.chat.id, 'help')

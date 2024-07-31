from telebot.types import Message
from ..config.config import commands
from api_telegramm_bot.core import bot


@bot.message_handler(commands=['help'])
def command_help(m: Message):
    cid = m.chat.id
    help_text = "Доступны следующие команды: \n"
    for key in commands:
        help_text += "/" + key + " - "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)

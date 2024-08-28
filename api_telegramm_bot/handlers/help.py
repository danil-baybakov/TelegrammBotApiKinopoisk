from telebot.types import Message
from ..config.config import commands
from api_telegramm_bot.core import bot
from api_database.core import api_db
from api_database.common.model import History


@bot.message_handler(commands=['help', 'start'])
def command_help(m: Message):
    cid = m.chat.id
    cmd = m.text
    help_text = "Доступны следующие команды: \n"
    for key in commands:
        help_text += "/" + key + " - "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)
    api_db.set_param_storage_by_cid(
        model=History,
        cid=cid,
        command=cmd
    )

from telebot.types import Message
from ..config.config import COMMANDS
from api_telegramm_bot.core import bot
from api_database.core import api_db
from api_database.common.model import History


@bot.message_handler(commands=['help', 'start'])
def command_help(message: Message) -> None:
    """
    Функция обработчика команд /help, /start
    для вывода справки по командам

    :param message: Объект сообщения
    """
    cid = message.chat.id  # id чата
    cmd = message.text  # текст сообщения

    # формируем и выводим в чат справку по всем командам
    help_text = "Доступны следующие команды: \n"
    for key in COMMANDS:
        help_text += "/" + key + " - "
        help_text += COMMANDS[key] + "\n"
    bot.send_message(cid, help_text)

    # сохраняем текущий запрос в БД в таблицу истории запросов
    api_db.set_param_storage_by_cid(
        model=History,
        cid=cid,
        command=cmd
    )

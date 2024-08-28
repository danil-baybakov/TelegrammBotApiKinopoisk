from telebot.types import Message
from api_database.core import api_db
from api_database.common.model import History
from api_telegramm_bot.core import bot


@bot.message_handler(commands=['history'])
def history(message: Message):
    cid = message.chat.id
    cmd = message.text
    list_history = api_db.get_history(model=History, cid=cid)
    content = '*История запросов:*\n------------------------------------------\n'
    if list_history:
        for index, value in enumerate(list_history):
            out = f'*{index+1}.* _[{value.timestamp.strftime('%H:%M:%S - %d.%m.%Y')}]_:  {value.command}'
            if value.limit is not None:
                out += f", кол-во: {value.limit}"
            if value.command == "/custom":
                out += f", рейтинг: ({value.min_rating}-{value.max_rating})"
            content += out + '\n'
    else:
        content += "Еще не было запросов..."
    bot.send_message(cid, content, parse_mode="Markdown")

    # api_db.set_param_storage_by_cid(
    #     model=History,
    #     cid=cid,
    #     command=cmd
    # )


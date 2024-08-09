from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from api_telegramm_bot.config.config import TOKEN

storage = StateMemoryStorage()

bot = TeleBot(token=TOKEN, state_storage=storage)

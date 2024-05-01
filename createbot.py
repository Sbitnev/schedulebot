from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

bottoken = 'ВАШ_ТОКЕН'
ADMINS_CHAT_ID = -9999 #ID_ЧАТА

storage = MemoryStorage()

bot = Bot(token=bottoken)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
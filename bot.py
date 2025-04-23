import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = '7581874786:AAEHu6aCqlQVfsFBgWp0eX_mvXwSKlw'

# Настроим логирование
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Применяем middleware для логирования
dp.middleware.setup(LoggingMiddleware())

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я твой бот.")

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Я помогу тебе с чем смогу!")

# Обработчик всех текстовых сообщений
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

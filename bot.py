import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import functools

API_TOKEN = '7581874786:AAEHu6aCqlQVfsFBgWp0eX_mvXwSKlw7W44'

# Настроим логирование
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Применяем middleware для логирования
dp.middleware.setup(LoggingMiddleware())

# Логирование отправки сообщений
_original_send_message = bot.send_message

async def logged_send_message(chat_id, text, *args, **kwargs):
    logging.info(f"[LOGGED SEND_MESSAGE] To: {chat_id}, Text: {text}")  # Логируем отправку
    return await _original_send_message(chat_id, text, *args, **kwargs)

bot.send_message = functools.partial(logged_send_message)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    logging.info(f"Получена команда /start от {message.from_user.id}")  # Логируем команду
    await message.reply("Привет! Я твой бот.")

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    logging.info(f"Получена команда /help от {message.from_user.id}")  # Логируем команду
    await message.reply("Я помогу тебе с чем смогу!")

# Обработчик всех текстовых сообщений
@dp.message_handler()
async def echo(message: types.Message):
    logging.info(f"Получено сообщение от {message.from_user.id}: {message.text}")  # Логируем сообщение
    await message.answer(f"Ты написал: {message.text}")

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

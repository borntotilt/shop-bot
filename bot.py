import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = 'ТВОЙ_ТОКЕН_ЗДЕСЬ'

# Логирование
logging.basicConfig(level=logging.INFO)

# Бот и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Клавиатура
main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add("Каталог товарів", "Часті питання")

# Обработчик /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привіт! Це демо-версія нашого бота. Обери, що тебе цікавить:",
        reply_markup=main_kb
    )

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Я допоможу тобі з чим зможу!")

# Каталог товарів
@dp.message_handler(lambda message: message.text == "Каталог товарів")
async def send_catalog(message: types.Message):
    text = (
        "**1. Вмонтована витяжка Mini Messer Pro**\n"
        "В комплекті 2 змінні мішки, має регулювання потужності, 65Вт.\n"
        "**Ціна:** 5000 грн\n\n"
        "**2. Мішки для витяжки**\n"
        "В наявності всі розміри. Для ваших настільних, педикюрних та врізних витяжок.\n"
        "**Ціна:**\n"
        "- 1 шт. — 140 грн\n"
        "- 5 шт. — 550 грн\n"
        "- 10 шт. — 900 грн"
    )
    await message.answer(text, parse_mode="Markdown")

# Часті питання
@dp.message_handler(lambda message: message.text == "Часті питання")
async def send_faq(message: types.Message):
    text = (
        "**1. Чи є гарантія на товари?**\n"
        "Так, є гарантія 1 рік на усі витяжки.\n\n"
        "**2. В який срок відправляються товари?**\n"
        "Відправка замовлення протягом 1-го робочого дня."
    )
    await message.answer(text, parse_mode="Markdown")

# Эхо для остальных сообщений
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ти написав: {message.text}")

# Удаление вебхука
async def on_start():
    await bot.delete_webhook()

# Запуск
if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_start())

    executor.start_polling(dp, skip_updates=True)

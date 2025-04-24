import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils import executor

API_TOKEN = 'ВАШ_ТОКЕН_ТУТ'

# Настроим логирование
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🛍️ Каталог товарів"),
    KeyboardButton("❓ Часті питання")
)

# /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Обери, що тебе цікавить:", reply_markup=main_menu)

# /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Я бот для демонстрації товарів. Натисни 'Каталог товарів' щоб побачити витяжки та мішки.")

# Каталог товарів
@dp.message_handler(lambda message: message.text == "🛍️ Каталог товарів")
async def send_catalog(message: types.Message):
    # 1 товар
    photo1 = "https://i.imgur.com/XXXXXXXX.jpg"  # вставь ссылку на фото
    caption1 = (
        "🌬️ *Вмонтована витяжка Mini Messer Pro*\n\n"
        "✅ Потужність: 65Вт\n"
        "📦 У комплекті: 2 змінні мішки\n"
        "⚙️ Регулювання потужності\n\n"
        "💰 *Ціна:* 5000 грн"
    )
    kb1 = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🛒 Купити", callback_data="buy_1")
    )
    await message.answer_photo(photo=photo1, caption=caption1, parse_mode="Markdown", reply_markup=kb1)

    # 2 товар
    photo2 = "https://i.imgur.com/YYYYYYYY.jpg"  # вставь вторую ссылку
    caption2 = (
        "🧺 *Мішки для витяжки*\n\n"
        "✅ В наявності всі розміри\n"
        "🧰 Для настільних, педикюрних та врізних витяжок\n\n"
        "💰 *Ціна:*\n"
        "- 1 шт. — 140 грн\n"
        "- 5 шт. — 550 грн\n"
        "- 10 шт. — 900 грн"
    )
    kb2 = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🛒 Купити", callback_data="buy_2")
    )
    await message.answer_photo(photo=photo2, caption=caption2, parse_mode="Markdown", reply_markup=kb2)

# Часті питання
@dp.message_handler(lambda message: message.text == "❓ Часті питання")
async def send_faq(message: types.Message):
    faq = (
        "📌 *Часті питання:*\n\n"
        "❓ _Чи є гарантія на товари?_\n"
        "✅ Так, є гарантія 1 рік на усі витяжки.\n\n"
        "❓ _В який срок відправляються товари?_\n"
        "✅ Відправка замовлення протягом 1-го робочого дня."
    )
    await message.answer(faq, parse_mode="Markdown")

# Обработчик кнопки "Купити"
@dp.callback_query_handler(lambda c: c.data and c.data.startswith("buy_"))
async def process_buy_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("Це демо. Купівля ще не реалізована.")

# Удаление вебхука при старте
async def on_start():
    await bot.delete_webhook()

# Запуск бота
if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_start())

    executor.start_polling(dp, skip_updates=True)

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    BotCommand
)
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '7581874786:AAEHu6aCqlQVfsFBgWp0eX_mvXwSKlw7W44'  # замени на свой токен

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# FSM стан для оформлення замовлення
class OrderForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_address = State()

# Меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🛍️ Каталог товарів"),
    KeyboardButton("❓ Часті питання")
)

back_to_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("↩️ Повернутися до меню")
)

async def set_commands(bot: Bot):
    commands = [
        BotCommand("start", "Запустити бота"),
        BotCommand("help", "Допомога"),
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Обери, що тебе цікавить:", reply_markup=main_menu)

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Я бот для демонстрації товарів. Натисни 'Каталог товарів', щоб побачити витяжки та мішки.")

@dp.message_handler(lambda message: message.text == "🛍️ Каталог товарів")
async def send_catalog(message: types.Message):
    photo1 = "https://i.imgur.com/gqXvcI6.jpeg"
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

    photo2 = "https://i.imgur.com/A22rY7L.jpeg"
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

    await bot.send_message(message.chat.id, "↩️ Натисни кнопку нижче, щоб повернутися до меню.", reply_markup=back_to_menu)

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
    await bot.send_message(message.chat.id, "↩️ Натисни кнопку нижче, щоб повернутися до меню.", reply_markup=back_to_menu)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("buy_"))
async def process_buy_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("Починаємо оформлення замовлення!")
    await OrderForm.waiting_for_name.set()
    await bot.send_message(callback_query.from_user.id, "Як вас звати?")

@dp.message_handler(state=OrderForm.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await OrderForm.next()
    await message.answer("Введіть, будь ласка, ваш номер телефону:")

@dp.message_handler(state=OrderForm.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await OrderForm.next()
    await message.answer("Введіть, будь ласка, вашу адресу доставки або напишіть 'Самовивіз':")

@dp.message_handler(state=OrderForm.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    phone = data['phone']
    address = message.text

    await message.answer(
        f"✅ Замовлення оформлено!\n\n"
        f"👤 Ім’я: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📍 Адреса: {address}\n\n"
        "Наш менеджер зв’яжеться з вами найближчим часом!"
    )
    await state.finish()

@dp.message_handler(lambda message: message.text == "↩️ Повернутися до меню")
async def back_to_main_menu(message: types.Message):
    await message.answer("Ти в головному меню:", reply_markup=main_menu)

async def on_start():
    await set_commands(bot)
    await bot.delete_webhook()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_start())
    executor.start_polling(dp, skip_updates=True)

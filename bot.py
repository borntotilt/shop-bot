import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    BotCommand
)
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

API_TOKEN = '7581874786:AAEHu6aCqlQVfsFBgWp0eX_mvXwSKlw7W44'  # замените на свой токен

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🛍️ Каталог товарів"),
    KeyboardButton("❓ Часті питання")
)

# Кнопка возврата
back_to_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("↩️ Повернутися до меню")
)

# Команды Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand("start", "Запустити бота"),
        BotCommand("help", "Допомога"),
    ]
    await bot.set_my_commands(commands)

# Состояния для оформления заказа
class OrderForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_address = State()

# Обработчики
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Обери, що тебе цікавить:", reply_markup=main_menu)

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Я бот для демонстрації товарів. Натисни 'Каталог товарів' щоб побачити витяжки та мішки.")

@dp.message_handler(lambda message: message.text == "🛍️ Каталог товарів")
async def send_catalog(message: types.Message):
    # Товар 1
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

    # Товар 2
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

    # Кнопка возврата
    await bot.send_message(message.chat.id, "↩️ Натисни кнопку нижче, щоб повернутися до меню.", reply_markup=back_to_menu)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('buy_'))
async def process_buy_callback(callback_query: types.CallbackQuery):
    product = callback_query.data.split('_')[1]
    await callback_query.answer(f"Вы выбрали товар: {product}")
    # Начинаем процесс оформления заказа
    await OrderForm.waiting_for_name.set()
    await bot.send_message(callback_query.from_user.id, "Пожалуйста, введите ваше имя:")

@dp.message_handler(state=OrderForm.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await OrderForm.next()
    await message.answer("Теперь введите ваш телефон:")

@dp.message_handler(state=OrderForm.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await OrderForm.next()
    await message.answer("Теперь введите ваш адрес (или укажите «Самовивіз» для самовывоза):")

@dp.message_handler(state=OrderForm.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    user_data = await state.get_data()
    name = user_data['name']
    phone = user_data['phone']
    address = user_data['address']

    # Подтверждение заказа
    await message.answer(f"Вы оформили заказ:\n\n"
                         f"Имя: {name}\n"
                         f"Телефон: {phone}\n"
                         f"Адрес: {address}\n\n"
                         "Спасибо за заказ!")
    await state.finish()  # Завершаем процесс оформления заказа

@dp.message_handler(lambda message: message.text == "↩️ Повернутися до меню")
async def back_to_main_menu(message: types.Message):
    await message.answer("Ти в головному меню:", reply_markup=main_menu)

# Удаление вебхука + установка команд
async def on_start():
    await set_commands(bot)
    await bot.delete_webhook()

# Запуск
if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_start())
    executor.start_polling(dp, skip_updates=True)

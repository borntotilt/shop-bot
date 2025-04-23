from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor

TOKEN = '7581874786:AAEHu6aCqlQVfsFBgWp0eX_mvXwSKlw7W44'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура с товарами
keyboard = InlineKeyboardMarkup(row_width=1)
keyboard.add(
    InlineKeyboardButton("Вмонтована витяжка Messer Pro - 5000 грн", callback_data="product1"),
    InlineKeyboardButton("Мішки для витяжки - від 140 грн", callback_data="product2")
)

@dp.message_handler(commands=['start', 'menu'])
async def start_command(message: types.Message):
    await message.answer("Ласкаво просимо! Оберіть товар:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data)
async def callback_handler(callback_query: types.CallbackQuery):
    if callback_query.data == "product1":
        await bot.send_message(callback_query.from_user.id,
            "Вмонтована витяжка Messer Pro\n65Вт, регулювання потужності.\nКомплект: 2 змінні мішки.\nЦіна: 5000 грн.")
    elif callback_query.data == "product2":
        await bot.send_message(callback_query.from_user.id,
            "Мішки для витяжки в наявності всі розміри:\n1 шт. - 140 грн\n5 шт. - 550 грн\n10 шт. - 900 грн.")

if __name__ == '__main__':
    executor.start_polling(dp)

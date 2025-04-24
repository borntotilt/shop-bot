from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dp.message_handler(lambda message: message.text == "Каталог товарів")
async def send_catalog(message: types.Message):
    # Первый товар
    photo1 = "https://i.imgur.com/XXXXXXXX.jpg"  # Сюда вставь прямую ссылку на фото
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

    # Второй товар
    photo2 = "https://i.imgur.com/YYYYYYYY.jpg"  # Сюда вставь вторую ссылку
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

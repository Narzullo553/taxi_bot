from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Taxilar = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📑 🔎 Ariza bo'yicha qidish"),
            KeyboardButton(text="🚕🚗 Barcha Automobillar")
        ],
        [
            KeyboardButton(text="🏠 Asosiy menu"),
            KeyboardButton(text="🔙 ortga")
        ]
    ], resize_keyboard=True
)
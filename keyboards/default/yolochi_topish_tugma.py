from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Yolovchilar_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📑 🔍 Ariza boʻyicha qidish"),
            KeyboardButton(text="🔍 Barcha yo'lovchilar")
        ],
        [
            KeyboardButton(text="🏠 Asosiy menu"),
            KeyboardButton(text="🔙 Ortga")
        ]
    ], resize_keyboard=True
)
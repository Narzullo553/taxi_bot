from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

yolovchi_tugma = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚖 Avtomobillar"),
            KeyboardButton(text="📃 Ariza qoldirish")
        ],
        [
            KeyboardButton(text="📑 Arizam"),
            KeyboardButton(text="🏠 Asosiy menu")
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)
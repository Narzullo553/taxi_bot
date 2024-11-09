from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tugma_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📃 Ro'yhatga yozilish"),
            KeyboardButton(text="📑 Malumot")
        ],
        [
            KeyboardButton(text="🙋🏻 Yoʻlovchilar"),
            KeyboardButton(text="🏠 Asosiy menu")
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)

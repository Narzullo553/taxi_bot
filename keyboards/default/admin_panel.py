from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Admin_panel = ReplyKeyboardMarkup(
    row_width=2,
    keyboard=[
        [
            KeyboardButton(text='Database'),
            KeyboardButton(text='reklama (advertising)'),
        ],
        [
            KeyboardButton(text='Admins'),
            KeyboardButton(text='Settings'),
        ],
        [
            KeyboardButton(text="Tozalash"),
            KeyboardButton(text="🏠 Asosiy menu")
        ]
    ],
    resize_keyboard=True
)
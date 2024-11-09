from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👥 Yo'lovchilar"),
            KeyboardButton(text="Haydovchilar 🚕")
        ],
        [
            KeyboardButton(text="Admins🧑🏻‍💻")
        ]
    ],resize_keyboard=True
)
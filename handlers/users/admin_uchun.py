from aiogram import types

from filters import IsAdmin_bot, IsPrivate
from keyboards.default.admin_panel import Admin_panel

from loader import dp, bot, db


@dp.message_handler(IsAdmin_bot(), IsPrivate(), text="Admins🧑🏻‍💻")
async def admins(msg: types.Message):
    await msg.answer(text="Adminlar bo'limiga o'tildi", reply_markup=Admin_panel)
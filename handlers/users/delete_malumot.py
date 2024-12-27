from filters import IsAdmin_bot
from loader import dp, db, bot
from aiogram import types
from data.config import ADMINS


@dp.message_handler(IsAdmin_bot(), commands=['clear'])
async def clear(msg: types.Message):
    try:
        await db.clear_time_taxi()
        await db.clear_time_yolovchi()
        await msg.answer("malumotlar o'chirildi")
    except Exception as eror:
        await bot.send_message(chat_id=ADMINS[0], text=eror)

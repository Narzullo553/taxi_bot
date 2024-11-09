from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.start_bot import Start_menu
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    fullname = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        users = await db.search_column(table='users', telegram_id=telegram_id)
        if users is None:
            user = await db.add_user(fullname, telegram_id)
            await bot.send_message(chat_id=ADMINS[0], text=f"fullname: {fullname}"
                                                           f"\ntelegram_id: {telegram_id}"
                                                           f"\n{user}")
    except Exception as error:
        user = error
        await bot.send_message(chat_id=ADMINS[0], text=user)

    await message.answer(f"Salom, {message.from_user.full_name}", reply_markup=Start_menu)


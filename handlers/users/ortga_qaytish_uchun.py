from aiogram import types
from data.config import ADMINS
from keyboards.default.haydovchilar_uchun_tugma import tugma_menu
from keyboards.default.start_bot import Start_menu
from keyboards.default.yolovchilar_uchun_tugma import yolovchi_tugma
from loader import dp, bot, db

@dp.message_handler(text="🏠 Asosiy menu")
async def Asosiy_menu(msg: types.Message):
    await msg.answer("Asosiy menuga qaytildi...", reply_markup=Start_menu)

@dp.message_handler(text="🔙 ortga")
async def habar2(msg: types.Message):
    await msg.answer("Ortga", reply_markup=yolovchi_tugma)

@dp.callback_query_handler(text='delete')
async def delete(call: types.CallbackQuery):
    try:
        delete = await db.delete_user(table='yolovchi', telegram_id=call.from_user.id)
        await call.message.answer(text="arizangiz o'chirildi")
        await call.message.delete()
    except Exception as error:
        await bot.send_message(chat_id=ADMINS[0], text=error)
@dp.callback_query_handler(text="delete1")
async def Ariza_ochir(call: types.CallbackQuery):
    try:
        delete = await db.delete_user(table='taxsis', telegram_id=call.from_user.id)
        await call.message.answer(text="arizangiz o'chirildi")
        await call.message.delete()
    except Exception as error:
        await bot.send_message(chat_id=ADMINS[0], text=error)
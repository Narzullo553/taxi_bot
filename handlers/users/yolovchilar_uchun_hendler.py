from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from data.Viloyat_tuman import Viloyat
from data.config import ADMINS
from keyboards.default.start_bot import Start_menu
from keyboards.default.yolovchilar_uchun_tugma import yolovchi_tugma
from keyboards.inline.Haydovchilar import Tugamalar_yaratish, Delete
from loader import dp, bot, db
import re

from states.yolovchilar_uchun_state import YOLOVCHILAR
nomerlar = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
soat = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
@dp.message_handler(text="📑 Arizam")
async def arizam(msg: types.Message):
    try:
        data = await db.search_column(table='yolovchi', telegram_id=msg.from_user.id)
        data = data[0]
        viloyatdan = data[0]
        tumandan = data[1]
        viloyatga = data[2]
        tumanga = data[3]
        tel_nomer = data[4]
        yurish_vaqti = data[5]
        text = (f"{viloyatdan} {tumandan}dan"
                f"\n{viloyatga} {tumanga}ga"
                f"\nsoat: {yurish_vaqti}"
                f"\ntelefon nomer: {tel_nomer}")
        await msg.answer(text, reply_markup=Delete)
    except:
        await msg.answer("malumotlar topilmadi")




@dp.message_handler(text="👥 Yo'lovchilar")
async def btn_next(msg: types.Message):
    await msg.answer("Yo'lovchilar bo'limiga o'tildi", reply_markup=yolovchi_tugma)

@dp.message_handler(text="📃 Ariza qoldirish")
async def ariza_olish(msg: types.Message):
    tugmalar = Tugamalar_yaratish(Viloyat.keys())
    await msg.answer("DIQQAT! BU KIRITISHDAN KEYIN, AVVAL KIRITGAN MALUMOTLARINGIZ YANGILANADI\n"
                     "YANGILANISHNI TO'XTATISH UCHUN ISTALGAN VAQTINGIZDA STOPNI BOSING"
                     "\nQuyidagi qaysi viloyatdan taxi qidirayapsiz", reply_markup=tugmalar)
    await YOLOVCHILAR.next()


@dp.callback_query_handler(text="stop", state=YOLOVCHILAR)
async def habar_yuborish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Ariza yozish to'xtatildi", reply_markup=yolovchi_tugma)
    await state.finish()

@dp.callback_query_handler(text=Viloyat.keys(),state=YOLOVCHILAR.viloyatdan)
async def viloyatdan(call: types.CallbackQuery, state: FSMContext):
    tugmalar = Tugamalar_yaratish(Viloyat[call.data])
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text="qaysi tumandan taxi qidirayapsiz", reply_markup=tugmalar)
    await state.update_data(
        {
            'viloyatdan': call.data
        }
    )
    await YOLOVCHILAR.next()
@dp.callback_query_handler(state=YOLOVCHILAR.tumandan)
async def tumandan(call: types.CallbackQuery, state: FSMContext):
    tugmalar = Tugamalar_yaratish(Viloyat.keys())
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text="Quyidagi qaysi viloyatga bormoqchisiz", reply_markup=tugmalar)
    await state.update_data(
        {
            'tumandan': call.data
        }
    )
    await YOLOVCHILAR.next()

@dp.callback_query_handler(state=YOLOVCHILAR.viloyatga)
async def viloyatga(call: types.CallbackQuery, state: FSMContext):
    tugmalar = Tugamalar_yaratish(Viloyat[call.data])
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text="Quyidagi qaysi tumanga bormoqchisiz", reply_markup=tugmalar)
    await state.update_data(
        {
            'viloyatga': call.data
        }
    )
    await YOLOVCHILAR.next()


@dp.callback_query_handler(state=YOLOVCHILAR.tumanga)
async def tumanga(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(
        {
            'tumanga': call.data
        }
    )
    await call.message.answer("tel nomeringizni kiriting", reply_markup=ReplyKeyboardRemove())
    await YOLOVCHILAR.next()




@dp.message_handler(state=YOLOVCHILAR.tel_nomer)
async def habar_yuborish4(msg: types.Message, state: FSMContext):
    if re.match(nomerlar, msg.text):
        await state.update_data(
            {'tel_nomer': msg.text}
        )
        await msg.answer("ketish vaqtingizni kiriting", reply_markup=ReplyKeyboardRemove())
        await YOLOVCHILAR.next()
    else:
        await msg.answer("Noto'g'ri nomer kiritildi \n qayta kiriting")

@dp.message_handler(state=YOLOVCHILAR.tel_nomer, content_types=types.ContentType.CONTACT)
async def nomer_olish(msg: types.Message, state: FSMContext):
    await state.update_data(
        {'tel_nomer': msg.contact.phone_number}
    )
    await msg.answer("mashina modelni kiriting", reply_markup=ReplyKeyboardRemove())
    await YOLOVCHILAR.next()



@dp.message_handler(state=YOLOVCHILAR.yurish_vaqti)
async def yurish_vaqti(msg: types.Message, state: FSMContext):
    if re.match(soat, msg.text):
        await state.update_data(
            {'yurish_vaqti': msg.text}
        )
        try:
            delete = await db.delete_user(table='yolovchi', telegram_id=msg.from_user.id)
            await bot.send_message(chat_id=ADMINS[0], text=delete)
        except Exception as error:
            await bot.send_message(chat_id=ADMINS[0], text=error)
        try:

            malumot = await state.get_data()
            viloyatdan = malumot['viloyatdan']
            tumandan = malumot['tumandan']
            viloyatga = malumot['viloyatga']
            tumanga = malumot['tumanga']
            tel_nomer = malumot['tel_nomer']
            yurish_vaqti = malumot['yurish_vaqti']
            telegram_id = msg.from_user.id
            insert = await db.add_yolovchi(viloyatdan,tumandan,viloyatga, tumanga,
                                           tel_nomer, yurish_vaqti, telegram_id)
            await bot.send_message(chat_id=ADMINS[0], text=insert)
        except Exception as error:
            await bot.send_message(chat_id=ADMINS[0], text=error)
        await msg.answer("kiritish yakunlandi", reply_markup=Start_menu)
        await state.finish()
    else:
        await msg.answer("Noto'g'ri soat kiritildi \n qayta kiriting")
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from data.Viloyat_tuman import Viloyat
from data.config import ADMINS
from keyboards.default.haydovchilar_uchun_tugma import tugma_menu
from keyboards.default.start_bot import Start_menu
from keyboards.inline.Haydovchilar import Tugamalar_yaratish, Delete1
from loader import dp, bot, db
from states.haydivchilar_uchun_stetes import HAYDOVCHI
import re
viloyat = {}

nomerlar = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
soat = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
@dp.message_handler(text="📑 Malumot")
async def habar_yuborish1(msg: types.Message):
    await msg.delete()
    try:
        data = await db.search_column(table='taxsis', telegram_id=msg.from_user.id)
        data = data[0]
        viloyatdan = data[0]
        tumandan = data[1]
        viloyatga = data[2]
        tumanga = data[3]
        moshina = data[4]
        tel_nomer = data[5]
        yurish_vaqti = data[6]
        text = (f"viloyatdan: {viloyatdan}"
                f"\ntumandan: {tumandan}"
                f"\nviloyatga: {viloyatga}"
                f"\ntumanga: {tumanga}"
                f"\n{moshina} rusumli avtomobil"
                f"\nyurish vaqti: {yurish_vaqti}"
                f"\ntelefon nomer: {tel_nomer}")
        await msg.answer(text, reply_markup=Delete1)
    except:
        await msg.answer("malumotlar topilmadi")


@dp.message_handler(text="Haydovchilar 🚕")
async def habar1(msg: types.Message):
    await msg.delete()
    await msg.answer("Quyidagi tugmadan birini tanlang", reply_markup=tugma_menu)


@dp.message_handler(text="📃 Ro'yhatga yozilish")
async def habar(msg: types.Message):
    tugmalar = Tugamalar_yaratish(Viloyat.keys())
    await msg.answer("DIQQAT! BU KIRITISHDAN KEYIN, AVVAL KIRITGAN MALUMOTLARINGIZ YANGILANADI\n"
                     "YANGILANISHNI TO'XTATISH UCHUN ISTALGAN VAQTINGIZDA STOPNI BOSING"
                     "\nQuyidagi qaysi viloyatdan \nyo'lovchi olmoqchisiz", reply_markup=tugmalar)
    await HAYDOVCHI.next()

@dp.callback_query_handler(text="stop", state=HAYDOVCHI)
async def habar_yuborish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("yolovchi olish to'xtatildi", reply_markup=tugma_menu)
    await state.finish()

@dp.callback_query_handler(text=Viloyat.keys(), state=HAYDOVCHI.viloyatdan)
async def habar_yuborish(call: types.CallbackQuery, state: FSMContext):
    tugmalar = Tugamalar_yaratish(Viloyat[call.data])
    await state.update_data(
        {
            'viloyatdan': call.data
        }
    )
    viloyat[call.from_user.id]=Viloyat[call.data]
    text = "Quyidagi qaysi tumandan "
    "\nyo'lovchi olmoqchisiz"
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=tugmalar)
    await HAYDOVCHI.next()


@dp.callback_query_handler(state=HAYDOVCHI.tumandan)
async def habar_yuborish1(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data in viloyat[call.from_user.id]:
            tugmalar = Tugamalar_yaratish(Viloyat.keys())
            await state.update_data(
                {'tumandan': call.data}
            )
            text = "Quyidagi qaysi viloyatga \nyo'lovchi olmoqchisiz"
            viloyat.pop(call.from_user.id)
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=tugmalar)
            await HAYDOVCHI.next()
    except:
        pass

@dp.callback_query_handler(text=Viloyat.keys(), state=HAYDOVCHI.viloyatga)
async def habar_yuborish2(call: types.CallbackQuery, state: FSMContext):
    tugmalar = Tugamalar_yaratish(Viloyat[call.data])
    await state.update_data(
        {'viloyatga': call.data}
    )
    viloyat[call.from_user.id] = Viloyat[call.data]
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f"Quyidagi qaysi tumanga"
                                                                                                  "\nyo'lovchi olmoqchisiz", reply_markup=tugmalar)
    await HAYDOVCHI.next()


@dp.callback_query_handler(state=HAYDOVCHI.tumanga)
async def habar_yuborish3(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data in viloyat[call.from_user.id]:
            await call.message.delete()
            await state.update_data(
                {'tumanga': call.data}
            )
            viloyat.pop(call.from_user.id)
            nomer = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)
                    ]
                ],
                resize_keyboard=True
            )
            await call.message.answer("tel nomerizni kiriting \nyoki tugmani bosing", reply_markup=nomer)
            await HAYDOVCHI.next()
    except:
        pass

@dp.message_handler(state=HAYDOVCHI.tel_nomer)
async def habar_yuborish4(msg: types.Message, state: FSMContext):
    if re.match(nomerlar, msg.text):
        await state.update_data(
            {'tel_nomer': msg.text}
        )
        await msg.answer("mashina modelni kiriting", reply_markup=ReplyKeyboardRemove())
        await HAYDOVCHI.next()
    else:
        await msg.answer("Nomerni to'g'ri kiriting")

@dp.message_handler(state=HAYDOVCHI.tel_nomer, content_types=types.ContentType.CONTACT)
async def nomer_olish(msg: types.Message, state: FSMContext):
    await state.update_data(
        {'tel_nomer': msg.contact.phone_number}
    )
    await msg.answer("mashina modelni kiriting", reply_markup=ReplyKeyboardRemove())
    await HAYDOVCHI.next()
@dp.message_handler(state=HAYDOVCHI.moshina)
async def habar_yuborish5(msg: types.Message, state: FSMContext):
    await state.update_data(
        {
            'mashina_modeli': msg.text}
    )
    await msg.answer("yurish vaqtingizni kiriting")
    await HAYDOVCHI.next()


@dp.message_handler(state=HAYDOVCHI.yurish_vaqti)
async def habar_yuborish6(msg: types.Message, state: FSMContext):
    if re.match(soat, msg.text):
        await state.update_data(
            {
                'yurish_vaqti': msg.text
            }
        )
        await msg.answer("kiritish yakunlandi", reply_markup=Start_menu)
        try:
            telegram_id = msg.from_user.id
            delete = await db.delete_user("taxsis", telegram_id)
            await bot.send_message(chat_id=ADMINS[0], text=delete)
        except Exception as e:
            await bot.send_message(chat_id=ADMINS[0], text=e)
        try:
            malumot = await state.get_data()
            viloyatdan = malumot['viloyatdan']
            tumandan = malumot['tumandan']
            viloyatga = malumot['viloyatga']
            tumanga = malumot['tumanga']
            tel_nomer = malumot['tel_nomer']
            moshina = malumot['mashina_modeli']
            yurish_vaqti = malumot['yurish_vaqti']
            telegram_id = msg.from_user.id
            taxi = await db.add_taxi(viloyatdan, tumandan, viloyatga, tumanga, moshina, tel_nomer, yurish_vaqti, telegram_id)
            await msg.answer(f"{viloyatdan} viloyati {tumandan} tumanidan "
                             f"\n{viloyatga} viloyati {tumanga} tumaniga"
                             f"\n{moshina} rusumli mashina"
                             f"\n{yurish_vaqti} da jo'naydi"
                             f"\ntel: {tel_nomer}"
                             f"\n{taxi}")
        except Exception as error:
            await bot.send_message(chat_id=ADMINS[0], text=error)
        try:
            await state.finish()
        except Exception as error:
            await bot.send_message(chat_id=ADMINS[0], text=error)
    else:
        await msg.answer("Noto'g'ri soat kiritildi \n qayta kiriting")



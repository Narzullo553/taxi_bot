from aiogram import types
from aiogram.dispatcher import FSMContext

from data.Viloyat_tuman import Viloyat
from handlers.users.Haydovchilar_uchun_hendler import viloyat
from keyboards.default.haydovchilar_uchun_tugma import tugma_menu
from keyboards.default.taxi_uchun_tugma import Taxilar
from keyboards.default.yolochi_topish_tugma import Yolovchilar_btn
from keyboards.inline.Haydovchilar import Tugamalar_yaratish
from loader import dp, bot, db
from states.haydivchilar_uchun_stetes import Taxi_topish

@dp.message_handler(text="🙋🏻 Yoʻlovchilar")
async def yolovchi_topish(msg: types.Message):
    await msg.answer("Yoʻlovchilar", reply_markup=Yolovchilar_btn)

@dp.message_handler(text="🔙 Ortga")
async def Ortga(msg: types.Message):
    await msg.answer("Ortga", reply_markup=tugma_menu)

@dp.message_handler(text="📑 🔍 Ariza boʻyicha qidish")
async def Yolovchilar1(msg: types.Message):
    try:
        data = await db.search_column(table='taxsis', telegram_id=msg.from_user.id)
        data = data[0]
        viloyatdan1 = data[0]
        tumandan1 = data[1]
        viloyatga1 = data[2]
        tumanga1 = data[3]
        yurish_vaqti1 = data[6]
        taxi = await db.search_column(table='yolovchi', viloyatdan=viloyatdan1, viloyatga=viloyatga1, tumandan=tumandan1,
                                      tumanga=tumanga1, yurish_vaqti=yurish_vaqti1)
        if taxi is not None:
            try:
                text = ''
                for data in taxi:
                    viloyatdan = data[0]
                    tumandan = data[1]
                    viloyatga = data[2]
                    tumanga = data[3]
                    tel_nomer = data[4]
                    yurish_vaqti = data[5]
                    text += (f"viloyatdan: {viloyatdan}"
                             f"\ntumandan: {tumandan}"
                             f"\nviloyatga: {viloyatga}"
                             f"\ntumanga: {tumanga}"
                             f"\nyurish vaqti: {yurish_vaqti}"
                             f"\ntelefon nomer: {tel_nomer}"
                             f"\n\n««««««««««««««»»»»»»»»»»»»»\n\n")
                await msg.answer(text)
            except:
                await msg.answer("malumotlar topilmadi")
        else:
            await msg.answer("malumotlar topilmadi")
    except:
        await msg.answer("malumotlar topilmadi")

@dp.message_handler(text="🔍 Barcha yo'lovchilar")
async def Yolovchilar1(msg: types.Message):
    tugamlar = Tugamalar_yaratish(Viloyat.keys())
    await msg.answer("Quyidagi qaysi viloyatdan \nyolovchi qidirayapsiz", reply_markup=tugamlar)
    await Taxi_topish.next()


@dp.callback_query_handler(text="stop", state=Taxi_topish)
async def habar_yuborish1(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("yolovchi olish to'xtatildi", reply_markup=Taxilar)
    await state.finish()


@dp.callback_query_handler(text=Viloyat.keys(), state=Taxi_topish.viloyatdan)
async def viloyatdan1(call: types.CallbackQuery, state: FSMContext):
    tugmalar = Tugamalar_yaratish(Viloyat[call.data])
    await state.update_data(
        {
            'viloyatdan': call.data
        }
    )
    viloyat[call.from_user.id] = Viloyat[call.data]
    text = "Quyidagi qaysi tumandan \nyolovchi qidirayapsiz"
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                reply_markup=tugmalar)
    await Taxi_topish.next()


@dp.callback_query_handler(state=Taxi_topish.tumandan)
async def habar_yuborish11(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data in viloyat[call.from_user.id]:
            tugmalar = Tugamalar_yaratish(Viloyat.keys())
            await state.update_data(
                {'tumandan': call.data}
            )
            text = "Quyidagi qaysi viloyatga borish uchun\n yolovchi qidirayapsiz"
            viloyat.pop(call.from_user.id)
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                        reply_markup=tugmalar)
            await Taxi_topish.next()
    except:
        pass


@dp.callback_query_handler(text=Viloyat.keys(), state=Taxi_topish.viloyatga)
async def habar_yuborish21(call: types.CallbackQuery, state: FSMContext):
    tugmalar = Tugamalar_yaratish(Viloyat[call.data])
    await state.update_data(
        {'viloyatga': call.data}
    )
    viloyat[call.from_user.id] = Viloyat[call.data]
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text=f"Quyidagi qaysi tumanga"
                                     "\nborish uchun yolovchi qidirayapsiz", reply_markup=tugmalar)
    await Taxi_topish.next()


@dp.callback_query_handler(state=Taxi_topish.tumanga)
async def habar_yuborish31(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data in viloyat[call.from_user.id]:
            await state.update_data(
                {'tumanga': call.data}
            )
            viloyat.pop(call.from_user.id)
            malumot = await state.get_data()
            viloyatdan1 = malumot['viloyatdan']
            tumandan1 = malumot['tumandan']
            viloyatga1 = malumot['viloyatga']
            tumanga1 = malumot['tumanga']
            taxi = await db.search_column(table='yolovchi', viloyatdan=viloyatdan1, viloyatga=viloyatga1,
                                          tumandan=tumandan1, tumanga=tumanga1)
            if taxi is not None:
                try:
                    text = ''
                    for data in taxi:
                        viloyatdan = data[0]
                        tumandan = data[1]
                        viloyatga = data[2]
                        tumanga = data[3]
                        tel_nomer = data[4]
                        yurish_vaqti = data[5]
                        text += (f"viloyatdan: {viloyatdan}"
                                 f"\ntumandan: {tumandan}"
                                 f"\nviloyatga: {viloyatga}"
                                 f"\ntumanga: {tumanga}"
                                 f"\nketish vaqti: {yurish_vaqti}"
                                 f"\ntelefon nomer: {tel_nomer}"
                                 f"\n\n««««««««««««««»»»»»»»»»»»»»\n\n")
                    await call.message.answer(text)
                except:
                    await call.message.answer("malumotlar topilmadi")
            await call.message.delete()
            await state.finish()
    except Exception as error:
        print(error)


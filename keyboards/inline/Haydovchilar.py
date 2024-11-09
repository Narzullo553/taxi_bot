from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def Tugamalar_yaratish(lugat):
    Haydovchilar_uchun = InlineKeyboardMarkup(row_width=2)
    for i in lugat:
        Haydovchilar_uchun.insert(InlineKeyboardButton(text=f"{i}", callback_data=i))
    Haydovchilar_uchun.insert(InlineKeyboardButton(text="stop", callback_data="stop"))
    return Haydovchilar_uchun

Delete = InlineKeyboardMarkup(row_width=1)
Delete.insert(InlineKeyboardButton(text="arizani o'chirish", callback_data="delete"))

Delete1 = InlineKeyboardMarkup(row_width=1)
Delete1.insert(InlineKeyboardButton(text="arizani o'chirish", callback_data="delete1"))
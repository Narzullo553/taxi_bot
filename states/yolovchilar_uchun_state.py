from aiogram.dispatcher.filters.state import StatesGroup, State

class YOLOVCHILAR(StatesGroup):
    viloyatdan = State()
    tumandan = State()
    viloyatga = State()
    tumanga = State()
    tel_nomer = State()
    yurish_vaqti = State()


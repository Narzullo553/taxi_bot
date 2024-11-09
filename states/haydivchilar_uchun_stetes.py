from aiogram.dispatcher.filters.state import StatesGroup, State

class HAYDOVCHI(StatesGroup):
    viloyatdan = State()
    tumandan = State()
    viloyatga = State()
    tumanga = State()
    tel_nomer = State()
    moshina = State()
    yurish_vaqti = State()

class Taxi_topish(StatesGroup):
    viloyatdan = State()
    tumandan = State()
    viloyatga = State()
    tumanga = State()



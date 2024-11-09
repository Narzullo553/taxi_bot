from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS


class IsAdmin_bot(BoundFilter):
    async def check(self, msg: types.Message) -> bool:
        return str(msg.from_user.id) in ADMINS
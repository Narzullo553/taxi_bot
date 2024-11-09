from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)
    await db.create()
    await db.create_table_users()
    await db.create_table_taxsis()
    await db.create_table_yolovchi()
    await on_startup_notify(dispatcher)
    # for i in ['taxsis', 'yolovchi']:
    #     izoh = await db.drop_table(i)
    #     print(izoh)
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

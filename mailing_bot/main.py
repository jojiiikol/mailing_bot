import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os

from dotenv import load_dotenv
from database import Database
from functions import func_users, func_services, func_admin

load_dotenv()
db = Database()
token = os.getenv('BOT_TOKEN')

bot = Bot(token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
print('Bot started')
async def main():


    dp = Dispatcher()
    dp.include_router(func_users.user_router)
    dp.include_router(func_services.services_router)
    dp.include_router(func_admin.admin_router)



    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

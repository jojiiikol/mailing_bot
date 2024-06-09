import asyncio
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os

from dotenv import load_dotenv
from database import Database
from functions import func_users, func_services, func_admin
from cheduler import Scheduler

load_dotenv()
db = Database()
scheduler = Scheduler()
token = os.getenv('BOT_TOKEN')
dp = Dispatcher()

bot = Bot(token=token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
print('Bot started')

async def test_ched():
    print("hello")

scheduler.add_job(test_ched, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=20))

async def main():
    scheduler.start()
    dp.include_router(func_users.user_router)
    dp.include_router(func_services.services_router)
    dp.include_router(func_admin.admin_router)
    print(scheduler.get_jobs())
    print(datetime.datetime.now())


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

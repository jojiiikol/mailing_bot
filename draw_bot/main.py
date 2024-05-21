import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os

from dotenv import load_dotenv

from database import Database

from functions import func_users

load_dotenv()
db = Database()
bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
print("Bot started")

async def main():
    dp = Dispatcher()
    dp.include_router(func_users.user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
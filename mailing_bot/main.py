import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types
from aiogram.filters import Command
import os

from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from database import Database
from functions import func_users, func_services

load_dotenv()
db = Database()
async def main():
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token=token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_router(func_users.user_router)
    dp.include_router(func_services.services_router)

    print('Bot started')

    @dp.callback_query(F.data == 'check_subscription')
    async def check_subscription(callback: types.CallbackQuery):
        await callback.answer()
        status = await bot.get_chat_member(chat_id=-1002092565895, user_id=callback.from_user.id)
        if status.status in ['left', 'kicked']:
            await callback.message.answer("К сожалению вы не подписаны, просим это сделать как можно быстрей!")
        else:
            await db.update_subscription_status_user(callback.from_user.id)
            await callback.message.answer("Спасибо за подписку, в скором времени мы будем отправлять тебе напоминалки о мероприятиях!")
            await callback.message.delete()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

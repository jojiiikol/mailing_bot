import __main__
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.user_kb import get_check_subscription_kb

user_router = Router()


@user_router.message(Command("start"))
async def start(message: types.Message):
    await __main__.db.insert_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"Привет, {message.from_user.username}, я бот, который будет оповещать тебя о предстоящем мероприятии!\n"
        f"Прошу подписаться тебя на канал https://t.me/djflkasdfhkjasldhfkjas. после того, как ты подпишешься, мы начнем работу!",
        reply_markup=get_check_subscription_kb().as_markup())


@user_router.callback_query(F.data == 'check_subscription')
async def check_subscription(callback: types.CallbackQuery):
    await callback.answer()
    status = await __main__.bot.get_chat_member(chat_id=-1002092565895, user_id=callback.from_user.id)
    if status.status in ['left', 'kicked']:
        await callback.message.answer("К сожалению вы не подписаны, просим это сделать как можно быстрей!")
    else:
        await __main__.db.update_subscription_status_user(callback.from_user.id)
        await callback.message.answer(
            "Спасибо за подписку, в скором времени мы будем отправлять тебе напоминалки о мероприятиях!")
        await callback.message.delete()

import __main__
from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards.user_kb import get_check_subscription_kb


user_router = Router()

@user_router.message(Command("start"))
async def start(message: types.Message):
    await __main__.db.insert_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Привет, {message.from_user.username}, я бот, который будет оповещать тебя о предстоящем мероприятии!\n"
                         f"Прошу подписаться тебя на группу (тут будет группа, ссылка), после того, как ты подпишешься, мы начнем работу!",
                         reply_markup=get_check_subscription_kb().as_markup())


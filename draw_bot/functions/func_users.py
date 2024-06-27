import __main__
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.user_kb import get_check_subscription_kb, get_sex_keyboard

user_router = Router()

class Registrations(StatesGroup):
    sex = State()


@user_router.message(Command('start'))
async def start(message: types.Message):
    user = await __main__.db.get_id_from_tg_id(message.from_user.id)
    if user:
        await  message.answer("Вы уже прошли этап регистрации")
    else:
        await __main__.db.insert_user(message.from_user.id, message.from_user.username)
        await message.answer(
            f"Привет, для участия в сегодняшнем розыгрыше просим подписаться на канал https://t.me/djflkasdfhkjasldhfkjas",
            reply_markup=get_check_subscription_kb().as_markup())


@user_router.callback_query(F.data == 'check_subscription')
async def check_subscription(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    status = await __main__.bot.get_chat_member(chat_id=-1002092565895, user_id=callback.from_user.id)
    if status.status in ['left', 'kicked']:
        await callback.message.answer("К сожалению вы не подписаны, просим это сделать как можно быстрее!")
    else:
        await callback.message.delete()
        await __main__.db.update_subscription_status_user(callback.from_user.id)
        await callback.message.answer("Отлично!\n\nТеперь укажите свой пол", reply_markup=get_sex_keyboard())
        await state.set_state(Registrations.sex)

@user_router.callback_query(Registrations.sex, F.data.contains("sex_"))
async def choose_sex(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[1]
    sex = None
    if data == "male":
        sex = "M"
    else:
        sex = "F"
    await __main__.db.update_sex_user(callback.from_user.id, sex)
    id_user = await __main__.db.get_id_from_tg_id(callback.from_user.id)
    await callback.message.answer(f"Отлично, ваше участие зачтено!\nВаш номер для розыгрыша - {id_user}")
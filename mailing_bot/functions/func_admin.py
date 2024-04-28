from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os
from dotenv import load_dotenv
from keyboards import admin_kb
import __main__

load_dotenv()
admin_router = Router()

# TODO: Просмотреть все трай эксепты, добавить новые.
# TODO: Добавить изменение рассылки
class CheckAdmin(StatesGroup):
    get_password = State()

class CreateMailing(StatesGroup):
    set_text = State()
    set_photo = State()
    confirm_1 = State()
    confirm_2 = State()
    confirm_3 = State()

@admin_router.message(F.text == "Открыть админ-панель")
async def get_admin(message: types.Message, state: FSMContext):
    await message.answer(text="Введите пароль")
    await state.set_state(CheckAdmin.get_password)

@admin_router.message(CheckAdmin.get_password)
async def get_password(message: types.Message, state: FSMContext):
    if message.text == os.getenv("ADMIN_PASSWORD"):
        await message.answer(text="Добро пожаловать в админ-панель", reply_markup=admin_kb.get_admin_keyboard())
        await __main__.db.insert_admin(message.from_user.id)
        await state.clear()
    else:
        await message.answer(text="Неверный пароль")
        await state.clear()

@admin_router.message(F.text == "Архив рассылок")
async def mailing_archive(message: types.Message):
    pass

@admin_router.message(F.text == "Создать рассылку")
async def create_mailing(message: types.Message, state: FSMContext):
    check_admin = await __main__.db.get_admin_id_from_tg_id(message.from_user.id)
    if check_admin == None:
        pass
    else:
        await message.answer(text="Создание рассылки идет в несколько этапов:\n"
                                  "1) Отправьте текст боту\n"
                                  "2) Бот запросит вас необходимость прикрепления фото - подтверждаете/отменяете\n"
                                  "3) После создания бот отправит пример рассылки\n"
                                  "4) Подтверждаете/отменяете\n"
                                  "5) Если все устраивает, нажимаете на кнопку 'Отправить сообщение'\n"
                                  "6) Снова подтверждаете/отменяете\n"
                                  "7) После подтверждения сообщение будет разослано пользователям")
        await message.answer(text="Отправьте текст будущей рассылки")
        await state.set_state(CreateMailing.set_text)

@admin_router.message(CreateMailing.set_text)
async def set_text(message: types.Message, state: FSMContext):
    text = message.html_text
    text = text.replace("'", '"')
    await message.answer(text="Необходимо ли фото к данной рассылке?", reply_markup=admin_kb.get_confirm_keyboard())
    await state.update_data(message_text = text)
    await state.set_state(CreateMailing.confirm_1)

@admin_router.callback_query(CreateMailing.confirm_1, F.data.contains("set_"))
async def confirm_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    callback_data = callback.data.split("_")[1]
    if callback_data == "confirm":
        await callback.message.answer(text="Отправьте фотографию")
        await state.set_state(CreateMailing.set_photo)
    if callback_data == "cancel":
        await state.update_data(photo=None)
        data = await state.get_data()
        await callback.message.answer(text=f"Пример рассылки: \n{data["message_text"]}", reply_markup=admin_kb.get_confirm_keyboard())
        await state.set_state(CreateMailing.confirm_2)

@admin_router.message(CreateMailing.set_photo, F.content_type == "photo")
async def set_photo(message: types.Message, state: FSMContext):
    try:
        photo = message.photo[0].file_id
        await state.update_data(photo=photo)
        await message.answer(text="Фотография принята")
        data = await state.get_data()
        message_text = data["message_text"]
        message_text += "\n\nПример рассылки"
        await message.answer_photo(photo=photo, caption=message_text, reply_markup=admin_kb.get_confirm_keyboard())
    except Exception as e:
        print(f"При подрузке фото произошла ошибка {str(e)}")
        await state.update_data(photo=None)
        await message.answer(text="Произошла ошибка при подгрузке фото")
    await state.set_state(CreateMailing.confirm_2)

@admin_router.callback_query(CreateMailing.confirm_2, F.data.contains("set_"))
async def confirm(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    message_text = data["message_text"]
    photo = data["photo"]
    callback_data = callback.data.split("_")[1]
    if callback_data == "confirm":
        users_for_mailing = await __main__.db.get_all_user_for_mailing()
        for user in users_for_mailing:
            try:
                if photo != None:
                    await __main__.bot.send_photo(chat_id=user[0], caption=message_text, photo=photo)
                else:
                    await __main__.bot.send_message(chat_id=user[0], text=message_text)
            except Exception as e:
                print(f"Ошибка во время отправки: {str(e)}")
        await callback.message.answer(text="Рассылка была проведена")
        await state.clear()
    if callback_data == "cancel":
        await callback.message.answer(text="Рассылка была отменена")
        await state.clear()
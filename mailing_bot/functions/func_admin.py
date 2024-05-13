import asyncio
import datetime
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os
from dotenv import load_dotenv
from keyboards import admin_kb
import __main__

load_dotenv()
admin_router = Router()


class CheckAdmin(StatesGroup):
    get_password = State()


class CreateMailing(StatesGroup):
    set_text = State()
    set_photo = State()
    edit_text = State()
    edit_photo = State()
    set_datetime = State()
    edit_datetime = State()
    confirm_1 = State()
    confirm_2 = State()
    confirm_3 = State()


@admin_router.message(Command("admin"))
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
    check_admin = await __main__.db.get_admin_id_from_tg_id(message.from_user.id)
    if check_admin is None:
        pass
    else:
        await message.answer(text="Выберите рассылку для просмотра",
                             reply_markup=admin_kb.get_archive_mailing_buttons())


@admin_router.callback_query(F.data.contains("archive_"))
async def get_archive(callback: types.CallbackQuery):
    await callback.answer()
    archive_message = callback.data.split("_")
    message = await __main__.db.get_archive_mailing_message(archive_message[1])
    photo = message[2]
    text = (f"Отправитель: {message[6]}\n"
            f"Дата отправления: {str(message[3])}\n"
            f"Время отправления: {str(message[4])}\n"
            f"Рассылка: {'Проведена' if message[5] == False else "Не проведена"}"
            f"\nТекст: {message[1]}")
    await callback.message.answer(text=text)

    try:
        if photo == 'None':
            pass
        else:
            await callback.message.answer_photo(photo=types.FSInputFile(path=photo))
    except Exception as e:
        print(f"Ошибка при отправке фото с сервера: {str(e)}")


@admin_router.message(F.text == "Создать рассылку")
async def create_mailing(message: types.Message, state: FSMContext):
    check_admin = await __main__.db.get_admin_id_from_tg_id(message.from_user.id)
    if check_admin is None:
        pass
    else:
        await message.answer(text="Создание рассылки идет в несколько этапов:\n"
                                  "1) Отправьте текст боту\n"
                                  "2) Бот запросит вас необходимость прикрепления фото - подтверждаете/отменяете\n"
                                  "3) Далее необходимо указать дату и время когда необходимо отправить сообщения \n"
                                  "4) После создания бот отправит пример рассылки\n"
                                  "5) Подтверждаете/отменяете\n"
                                  "6) Если все устраивает, нажимаете на кнопку 'Подтвердить'\n"
                                  "7) После подтверждения сообщение будет разослано пользователям")
        await message.answer(text="Отправьте текст будущей рассылки")
        await state.set_state(CreateMailing.set_text)


@admin_router.message(CreateMailing.set_text)
async def set_text(message: types.Message, state: FSMContext):
    text = replace_quotes(message.html_text)
    if len(text) > 1024:
        await message.answer(
            text="Ограничения telegram не позволяют отправить сообщение более 1024 символов\nОтправьте новый текст")
        await state.set_state(CreateMailing.set_text)
    else:
        await message.answer(text="Необходимо ли фото к данной рассылке?", reply_markup=admin_kb.get_confirm_keyboard())
        await state.update_data(message_text=text)
        await state.set_state(CreateMailing.confirm_1)


@admin_router.callback_query(CreateMailing.confirm_1, F.data.contains("set_"))
async def confirm_photo_need(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    callback_data = callback.data.split("_")[1]

    if callback_data == "confirm":
        await callback.message.answer(text="Отправьте фотографию")
        await state.set_state(CreateMailing.set_photo)

    if callback_data == "cancel":
        await state.update_data(photo=None)
        await state.update_data(photo_info=None)
        await callback.message.answer(text="Введите дату и время в формате: 10.05 12:59")
        await state.set_state(CreateMailing.set_datetime)


@admin_router.message(CreateMailing.set_photo, F.content_type == "photo")
async def set_photo(message: types.Message, state: FSMContext):
    try:
        photo_id = get_photo_id_from_message(message)
        photo_info = get_photo_info_from_message(message)

        await state.update_data(photo=photo_id)
        await state.update_data(photo_info=photo_info)

        await message.answer(text="Фотография принята")
    except Exception as e:
        print(f"При подрузке фото произошла ошибка {str(e)}")

        await state.update_data(photo=None)
        await state.update_data(photo_info=None)
        await message.answer(text="Произошла ошибка при подгрузке фото")

    await message.answer(text="Введите дату и время в формате: 10.05 12:59")
    await state.set_state(CreateMailing.set_datetime)


@admin_router.message(CreateMailing.set_datetime)
async def set_date(message: types.Message, state: FSMContext):
    try:
        date = message.text.split(" ")[0]
        time = message.text.split(" ")[1]
        datetimes = datetime.datetime(
            year=datetime.datetime.now().year,
            month=int(date.split(".")[1]),
            day=int(date.split(".")[0]),
            hour=int(time.split(":")[0]),
            minute=int(time.split(":")[1]),
            second=0
        )
        if datetime.datetime.now() > datetimes:
            await message.answer(text="Неверно введенные дата и время (прошедшая дата)")
            await message.answer(text="Введите дату и время в формате: 10.05 12:59")
            await state.set_state(CreateMailing.set_datetime)
        else:
            await state.update_data(date=datetimes)
            await message.answer(text="Дата и время приняты")
            await send_example_mailing(state, message)
            await state.set_state(CreateMailing.confirm_2)
    except Exception as e:
        print(f"При установке даты произошла ошибка: {str(e)}")
        await message.answer(text="Произошла ошибка, повторите попытку")
        await message.answer(text="Введите дату и время в формате: 10.05 12:59")
        await state.set_state(CreateMailing.set_datetime)


@admin_router.callback_query(CreateMailing.confirm_2, F.data.contains("edit_"))
async def edit_data(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    callback_data = callback.data.split("_")[1]
    if callback_data == "text":
        await callback.message.answer(text="Введите новый текст")
        await state.set_state(CreateMailing.edit_text)
    if callback_data == "photo":
        await callback.message.answer(text="Отправьте новое фото")
        await state.set_state(CreateMailing.edit_photo)
    if callback_data == "datetime":
        await callback.message.answer(text="Отправьте новое время и дату\nФормат: 10.05 01:59")
        await state.set_state(CreateMailing.edit_datetime)


@admin_router.message(CreateMailing.edit_text)
async def edit_text(message: types.Message, state: FSMContext):
    text = replace_quotes(message.html_text)
    if len(text) > 1024:
        await message.answer(
            text="Ограничения telegram не позволяют отправить сообщение более 1024 символов\nОтправьте новый текст")
        await state.set_state(CreateMailing.set_text)
    else:
        await state.update_data(message_text=text)
        await send_example_mailing(state, message)
        await state.set_state(CreateMailing.confirm_2)


@admin_router.message(CreateMailing.edit_photo)
async def edit_photo(message: types.Message, state: FSMContext):
    try:
        photo = get_photo_id_from_message(message)
        await state.update_data(photo=photo)
        await state.update_data(photo_info=message.photo[-1])
        await message.answer(text="Фотография принята")
        await send_example_mailing(state, message)
    except Exception as e:
        print(f"При подрузке фото произошла ошибка {str(e)}")
        await state.update_data(photo=None)
        await state.update_data(photo_info=None)
        await message.answer(text="Произошла ошибка при подгрузке фото")
        await send_example_mailing(state, message)
    await state.set_state(CreateMailing.confirm_2)


@admin_router.message(CreateMailing.edit_datetime)
async def edit_datetime(message: types.Message, state: FSMContext):
    try:
        date = message.text.split(" ")[0]
        time = message.text.split(" ")[1]
        datetimes = datetime.datetime(
            year=datetime.datetime.now().year,
            month=int(date.split(".")[1]),
            day=int(date.split(".")[0]),
            hour=int(time.split(":")[0]),
            minute=int(time.split(":")[1]),
            second=0
        )
        if datetime.datetime.now() > datetimes:
            await message.answer(text="Неверно введенные дата и время (прошедшая дата)")
            await message.answer(text="Введите дату и время в формате: 10.05 12:59")
            await state.set_state(CreateMailing.edit_datetime)
        else:
            await state.update_data(date=datetimes)
            await message.answer(text="Дата и время приняты")
            await send_example_mailing(state, message)
            await state.set_state(CreateMailing.confirm_2)
    except Exception as e:
        print(f"Произошла ошибка при изменении даты и времени: {str(e)}")
        await message.answer(text="Произошла ошибка, повторите попытку")
        await message.answer(text="Отправьте новое время и дату\nФормат: 10.05 01:59")
        await state.set_state(CreateMailing.edit_datetime)


@admin_router.callback_query(CreateMailing.confirm_2, F.data.contains("set_"))
async def do_mailing(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await download_photo_to_server(data['photo_info'])
    await insert_mailing_in_archive(callback.from_user.id, state)
    await make_mailing_job_for_cheduler(state)
    await state.clear()


async def make_mailing_job_for_cheduler(state: FSMContext):
    message_text, photo, date = await get_mailing_data(state)
    __main__.scheduler.add_job(mailing, 'date', run_date=date, args=(message_text, photo))
    print("Добавлена задача в планировщик")
    print(f"Всего задач: {len(__main__.scheduler.get_jobs())}\n")


async def mailing(message_text, photo):
    users = await __main__.db.get_all_user_for_mailing()
    if photo is not None:
        for user in users:
            try:
                await __main__.bot.send_photo(chat_id=user[0], caption=message_text, photo=photo)
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"Ошибка во время отправки: {str(e)}")
    else:
        for user in users:
            try:
                await __main__.bot.send_message(chat_id=user[0], text=message_text)
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"Ошибка во время отправки: {str(e)}")
    try:
        await __main__.db.change_status_mailing(message_text)
    except Exception as e:
        print(f"Произошла ошибка при смене статуса рассылки: {str(e)}")


async def insert_mailing_in_archive(tg_id, state: FSMContext):
    try:
        data = await state.get_data()
        message_text, photo_id, dates = await get_mailing_data(state)
        photo = data["photo_info"]
        time = dates.time()
        date = dates.date()
        if photo is not None:
            photo_name = f"photo/{get_photo_id(photo)}.jpg"
        else:
            photo_name = None
        await __main__.db.insert_mailing_in_db(tg_id, text=message_text, photo=photo_name, time=time, date=date)
    except Exception as e:
        print(f"Произошла ошибка при внесении данных о рассылке в БД: {str(e)}")


async def download_photo_to_server(photo):
    if photo is None:
        pass
    else:
        try:
            file = await __main__.bot.get_file(photo.file_id)
            file_path = file.file_path
            await __main__.bot.download_file(file_path=file_path,
                                             destination=f"photo/{get_photo_name_from_photo_id(photo)}")
        except Exception as e:
            print(f"Произошла ошибка при скачивании фото на сервер: {str(e)}")


async def get_mailing_data(state: FSMContext):
    data = await state.get_data()
    message_text = data['message_text']
    photo_id = data['photo']
    date = data['date']
    return message_text, photo_id, date


async def send_example_mailing(state: FSMContext, message: types.Message):
    message_text, photo_id, date = await get_mailing_data(state=state)
    full_message_text = f"ПРИМЕР РАССЫЛКИ НА {date}: \n {message_text}"
    if photo_id is not None:
        full_message_text = full_message_text[:1023]
        await message.answer_photo(photo=photo_id, caption=full_message_text, reply_markup=admin_kb.get_edit_keyboard())
    else:
        await message.answer(text=full_message_text, reply_markup=admin_kb.get_edit_keyboard())


def get_photo_id(photo):
    return photo.file_unique_id


def get_photo_name_from_photo_id(photo):
    return get_photo_id(photo) + ".jpg"


def get_photo_id_from_message(message: types):
    photo_info = get_photo_info_from_message(message)
    return photo_info.file_id


def get_photo_info_from_message(message: types.Message):
    return message.photo[-1]


def replace_quotes(text):
    return text.replace("'", '"')

import asyncio

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
    text = replace_quotes(message.html_text)
    await message.answer(text="Необходимо ли фото к данной рассылке?", reply_markup=admin_kb.get_confirm_keyboard())
    await state.update_data(message_text=text)
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
        await state.update_data(photo_info=None)
        data = await state.get_data()
        await callback.message.answer(text=f"Пример рассылки: \n{data["message_text"]}",
                                      reply_markup=admin_kb.get_edit_keyboard())
        await state.set_state(CreateMailing.confirm_2)


@admin_router.message(CreateMailing.set_photo, F.content_type == "photo")
async def set_photo(message: types.Message, state: FSMContext):
    try:
        photo_id = get_photo_id_from_message(message)
        photo_info = get_photo_info_from_message(message)

        await state.update_data(photo=photo_id)
        await state.update_data(photo_info=photo_info)
        data = await state.get_data()

        await message.answer(text="Фотография принята")

        message_text = data["message_text"]
        message_text += "\n\nПример рассылки"
        await message.answer_photo(photo=photo_id, caption=message_text, reply_markup=admin_kb.get_edit_keyboard())
    except Exception as e:
        print(f"При подрузке фото произошла ошибка {str(e)}")

        await state.update_data(photo=None)
        await state.update_data(photo_info=None)
        await message.answer(text="Произошла ошибка при подгрузке фото")

        data = await state.get_data()
        message_text = data["message_text"]
        await message.answer(text=message_text, reply_markup=admin_kb.get_edit_keyboard())

    await state.set_state(CreateMailing.confirm_2)


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


@admin_router.message(CreateMailing.edit_text)
async def edit_text(message: types.Message, state: FSMContext):
    photo_id = get_photo_id_from_message(message)
    photo_info = get_photo_info_from_message(message)

    text = replace_quotes(message.html_text)
    await state.update_data(message_text=text)
    data = await state.get_data()
    if photo_id == None:
        await message.answer(text=f"Пример рассылки:\n{data['message_text']}",
                             reply_markup=admin_kb.get_edit_keyboard())
    else:
        await message.answer_photo(photo=photo_id, caption=f"{data["message_text"]}\n\nПример рассылки",
                                   reply_markup=admin_kb.get_edit_keyboard())
    await state.set_state(CreateMailing.confirm_2)


@admin_router.message(CreateMailing.edit_photo)
async def edit_photo(message: types.Message, state: FSMContext):
    try:
        photo = get_photo_id_from_message(message)
        await state.update_data(photo=photo)
        await state.update_data(photo_info=message.photo[-1])
        await message.answer(text="Фотография принята")
        data = await state.get_data()
        message_text = data["message_text"]
        message_text += "\n\nПример рассылки"
        await message.answer_photo(photo=photo, caption=message_text, reply_markup=admin_kb.get_edit_keyboard())
    except Exception as e:
        print(f"При подрузке фото произошла ошибка {str(e)}")
        await state.update_data(photo=None)
        await state.update_data(photo_info=None)
        await message.answer(text="Произошла ошибка при подгрузке фото")
        data = await state.get_data()
        message_text = data["message_text"]
        await message.answer(text=message_text, reply_markup=admin_kb.get_edit_keyboard())
    await state.set_state(CreateMailing.confirm_2)


@admin_router.callback_query(CreateMailing.confirm_2, F.data.contains("set_"))
async def confirm(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    message_text = data["message_text"]
    photo = data["photo"]
    print(photo)
    photo_info = data["photo_info"]
    callback_data = callback.data.split("_")[1]
    if callback_data == "confirm":
        await download_photo_to_server(photo_info)
        users_for_mailing = await __main__.db.get_all_user_for_mailing()
        time_for_mailing = len(users_for_mailing) * 1.5
        await callback.message.answer(text=f"Примерное время рассылки каждому участнику: {time_for_mailing} ~ секунд")
        await mailing(users_for_mailing, photo, message_text)
        await callback.message.answer(text="Рассылка была проведена")
        await insert_mailing_in_archive(callback.from_user.id, data)
        await state.clear()
    if callback_data == "cancel":
        await callback.message.answer(text="Рассылка была отменена")
        await state.clear()


async def mailing(users, photo, message_text):
    if photo != None:
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


async def insert_mailing_in_archive(tg_id, data):
    try:
        photo = data["photo_info"]
        if photo != None:
            photo_name = get_photo_id(photo)
        else:
            photo_name = None
        message_text = data["message_text"]
        await __main__.db.insert_mailing_in_archive(tg_id, text=message_text, photo=photo_name)
    except Exception as e:
        print(f"Произошла ошибка при внесении данных о рассылке в БД: {str(e)}")


async def download_photo_to_server(photo):
    if photo == None:
        pass
    else:
        try:
            file = await __main__.bot.get_file(photo.file_id)
            file_path = file.file_path
            new_photo = await __main__.bot.download_file(file_path=file_path,
                                                         destination=f"{get_photo_name_from_photo_id(photo)}")
        except Exception as e:
            print(f"Произошла ошибка при скачивании фото на сервер: {str(e)}")


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
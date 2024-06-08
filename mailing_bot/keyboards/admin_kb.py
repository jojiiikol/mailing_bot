from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder, InlineKeyboardButton
import __main__


class Paginator(CallbackData, prefix="pag"):
    action: str
    page: int


def get_admin_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Архив рассылок")
    kb.button(text="Создать рассылку")
    return kb.as_markup(resize_keyboard=True)


def get_confirm_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Подтвердить", callback_data="set_confirm")
    kb.button(text="Отменить", callback_data="set_cancel")
    return kb.as_markup()


def get_edit_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Изменить текст", callback_data="edit_text")
    kb.button(text="Изменить фото", callback_data="edit_photo")
    kb.button(text="Изменить время и дату", callback_data="edit_datetime")
    kb.button(text="Подтвердить", callback_data="set_confirm")
    kb.button(text="Отменить", callback_data="set_cancel")
    kb.adjust(2, 1, 2)
    return kb.as_markup()


def get_archive_mailing_buttons(page: int):
    kb = InlineKeyboardBuilder()
    mailing_messages = __main__.db.get_archive_mailing_kb()

    limit = 5
    start_offset = page * limit
    end_offset = start_offset + limit

    for message in mailing_messages[start_offset:end_offset]:
        kb.button(text=f"{message[0]}: {message[1][:30]}...", callback_data=f"archive_{message[2]}")

    if page > 0:
        kb.button(text="Назад", callback_data=Paginator(page=page - 1, action="next").pack())
    if end_offset < len(mailing_messages):
        kb.button(text="Вперед", callback_data=Paginator(page=page + 1, action="prev").pack())

    kb.adjust(*[1 for x in range(0, 5)], 2)

    return kb.as_markup()

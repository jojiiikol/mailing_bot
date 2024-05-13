from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder, InlineKeyboardButton
import __main__

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
    kb.adjust(2, 3)
    return kb.as_markup()

def get_archive_mailing_buttons():
    kb = InlineKeyboardBuilder()
    mailing_messages = __main__.db.get_archive_mailing_kb()
    for message in mailing_messages:
        kb.button(text=f"{message[0]}: {message[1][:10]}...", callback_data=f"archive_{message[2]}")
    kb.adjust(1, 1)
    return kb.as_markup()
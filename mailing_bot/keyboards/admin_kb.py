from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder, InlineKeyboardButton

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
def get_mailing_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Отправить сообщение", callback_data="send")
    return kb.as_markup()
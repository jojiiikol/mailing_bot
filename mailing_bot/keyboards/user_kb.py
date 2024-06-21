from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_check_subscription_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Проверить подписку", callback_data="check_subscription")
    return builder

def get_main_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="О фестивале", callback_data="about_festival")
    kb.button(text="Логистика", callback_data="logistic")
    # kb.button(text="Навигация", callback_data="navigation")
    kb.button(text="Программа недели молодежи", callback_data="program")
    kb.button(text="Программа дня молодежи", callback_data="molod_day")
    kb.button(text="Розыгрыш", callback_data="draw")
    kb.button(text="Связаться с организатором", url="https://vk.com/molodnv")
    kb.adjust(1)
    return kb.as_markup()

def get_back_button(photo_id=0):
    data = f"back_to_main_{photo_id}"
    kb = InlineKeyboardBuilder()
    kb.button(text="На главное меню", callback_data=data)
    return kb.as_markup()

def get_back_from_event_button():
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data="back_to_event")
    return kb.as_markup()

def get_program_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="24 июня", callback_data="june_24")
    kb.button(text="25 июня", callback_data="june_25")
    kb.button(text="26 июня", callback_data="june_26")
    kb.button(text="27 июня", callback_data="june_27")
    kb.button(text="28 и 29 июня", callback_data="june_28")
    # kb.button(text="29 июня", callback_data="june_29")
    kb.button(text="На главное меню", callback_data="back_to_main_0")
    kb.adjust(1)
    return kb.as_markup()

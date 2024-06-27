from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_check_subscription_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Проверить подписку", callback_data="check_subscription")
    return builder

def get_sex_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="М", callback_data="sex_male")
    builder.button(text="Ж", callback_data="sex_female")
    builder.adjust(2)
    return builder.as_markup()
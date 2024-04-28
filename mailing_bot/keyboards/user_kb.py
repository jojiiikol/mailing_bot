from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_check_subscription_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Проверить подписку", callback_data="check_subscription")
    return builder
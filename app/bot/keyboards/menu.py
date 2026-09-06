from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⭐ Join VIP"), KeyboardButton(text="💳 Payment")],
            [KeyboardButton(text="📋 My Subscription"), KeyboardButton(text="👤 Contact Admin")],
            [KeyboardButton(text="🔄 Restart")],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )

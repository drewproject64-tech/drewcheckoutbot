from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="lang:it")],
        [InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang:fr")],
        [InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="lang:de")],
    ])


def back_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔄 Restart")]], resize_keyboard=True)

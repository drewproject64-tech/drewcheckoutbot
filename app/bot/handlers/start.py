from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards.navigation import language_keyboard
from app.locales import get_text

router = Router(name="start")


@router.message(CommandStart())
async def start(message: Message, user):
    await message.answer(get_text("welcome", user.language), reply_markup=language_keyboard())

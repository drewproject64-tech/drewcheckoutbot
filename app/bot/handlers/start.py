from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards.navigation import language_keyboard
from app.database.repositories import upsert_user
from app.locales import get_text

router = Router(name="start")


@router.message(CommandStart())
async def start(message: Message, db_session):
    user = await upsert_user(db_session.session, message.from_user)
    await db_session.session.commit()
    await message.answer(get_text("welcome", user.language), reply_markup=language_keyboard())

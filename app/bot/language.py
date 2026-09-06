from aiogram import Router
from aiogram.types import CallbackQuery

from app.bot.keyboards.menu import main_menu
from app.locales import get_text

router = Router(name="language")


@router.callback_query(lambda c: bool(c.data and c.data.startswith("lang:")))
async def select_language(callback: CallbackQuery, user, db_session):
    language = callback.data.split(":", 1)[1]
    if language not in {"en", "it", "fr", "de"}:
        await callback.answer("Invalid language", show_alert=True)
        return
    user.language = language
    await db_session.commit()
    await callback.message.answer(get_text("language_saved", language), reply_markup=main_menu())
    await callback.answer()

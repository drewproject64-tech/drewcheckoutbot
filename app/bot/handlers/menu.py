from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.keyboards.menu import main_menu
from app.bot.keyboards.navigation import language_keyboard
from app.bot.keyboards.plans import plans_keyboard
from app.locales import get_text
from app.services.subscription_service import format_subscription_status

router = Router(name="menu")


@router.message(F.text == "⭐ Join VIP")
async def join_vip(message: Message, user, settings):
    await message.answer(get_text("join_vip", user.language), reply_markup=plans_keyboard(settings.plans))


@router.message(F.text == "💳 Payment")
async def payment_menu(message: Message, user, settings):
    await message.answer(get_text("payment_choose", user.language), reply_markup=plans_keyboard(settings.plans))


@router.message(F.text == "📋 My Subscription")
async def my_subscription(message: Message, user, db_session, settings):
    text = await format_subscription_status(db_session, user, settings)
    await message.answer(text, reply_markup=main_menu())


@router.message(F.text == "👤 Contact Admin")
async def contact_admin(message: Message, user, settings):
    await message.answer(get_text("contact_admin", user.language, contact=settings.admin_contact), reply_markup=main_menu())


@router.message(F.text == "🔄 Restart")
async def restart(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(get_text("restart", "en"), reply_markup=language_keyboard())

from __future__ import annotations

from decimal import Decimal

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.exc import IntegrityError

from app.bot.keyboards.admin import payment_review_keyboard
from app.bot.keyboards.menu import main_menu
from app.bot.states import PaymentForm
from app.database.models import Payment, PaymentStatus
from app.database.repositories import tx_hash_exists
from app.locales import get_text

router = Router(name="payments")


def _plan(settings, key: str):
    return settings.plans.get(key)


@router.callback_query(lambda c: bool(c.data and c.data.startswith("plan:")))
async def select_plan(callback: CallbackQuery, state: FSMContext, user, settings):
    plan_key = callback.data.split(":", 1)[1]
    plan = _plan(settings, plan_key)
    if plan is None:
        await callback.answer(get_text("invalid_plan", user.language), show_alert=True)
        return

    await state.clear()
    await state.update_data(plan_key=plan_key, expected_amount=float(plan["price"]), user_id=user.id, language=user.language)
    await state.set_state(PaymentForm.waiting_screenshot)
    await callback.message.answer(
        get_text(
            "payment_instructions", user.language,
            plan=plan["name"], amount=float(plan["price"]), network=settings.payment_network, wallet=settings.usdt_wallet,
        ),
        reply_markup=main_menu(),
    )
    await callback.answer()


@router.message(PaymentForm.waiting_screenshot, F.photo)
async def receive_screenshot(message: Message, state: FSMContext):
    data = await state.get_data()
    screenshot_file_id = message.photo[-1].file_id
    await state.update_data(screenshot_file_id=screenshot_file_id)
    await state.set_state(PaymentForm.waiting_tx_hash)
    await message.answer(get_text("screenshot_received", data.get("language", "en")))


@router.message(PaymentForm.waiting_screenshot)
async def invalid_screenshot(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(get_text("send_screenshot", data.get("language", "en")))


@router.message(PaymentForm.waiting_tx_hash, F.text)
async def receive_tx_hash(message: Message, state: FSMContext, user, db_session, settings, bot):
    tx_hash = message.text.strip()
    if not 8 <= len(tx_hash) <= 255:
        await message.answer(get_text("invalid_tx", user.language))
        return

    if await tx_hash_exists(db_session, tx_hash):
        await message.answer(get_text("duplicate_tx", user.language))
        return

    data = await state.get_data()
    plan_key = data.get("plan_key")
    plan = _plan(settings, plan_key or "")
    screenshot_file_id = data.get("screenshot_file_id")
    if plan is None or not screenshot_file_id:
        await state.clear()
        await message.answer(get_text("invalid_plan", user.language), reply_markup=main_menu())
        return

    payment = Payment(
        user_id=user.id,
        plan_key=plan_key,
        amount=Decimal(str(float(plan["price"]))),
        currency="USDT",
        network=settings.payment_network,
        wallet_address=settings.usdt_wallet,
        screenshot_file_id=screenshot_file_id,
        transaction_hash=tx_hash,
        status=PaymentStatus.PENDING.value,
    )
    db_session.add(payment)
    try:
        await db_session.flush()
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        await message.answer(get_text("duplicate_tx", user.language))
        return

    username = f"@{user.username}" if user.username else "—"
    caption = (
        "💳 New Payment Pending\n\n"
        f"Payment ID: #{payment.id}\n"
        f"User: {user.first_name or 'Unknown'}\n"
        f"Username: {username}\n"
        f"Telegram ID: {user.telegram_id}\n\n"
        f"Plan: {plan['name']}\n"
        f"Amount: ${float(plan['price']):.2f} USDT\n"
        f"Network: {settings.payment_network}\n\n"
        f"Transaction hash:\n{tx_hash}"
    )
    for admin_id in settings.admin_ids:
        try:
            await bot.send_photo(
                admin_id,
                payment.screenshot_file_id,
                caption=caption,
                reply_markup=payment_review_keyboard(payment.id),
            )
        except Exception:
            continue

    await state.clear()
    await message.answer(get_text("payment_submitted", user.language, payment_id=payment.id), reply_markup=main_menu())


@router.message(PaymentForm.waiting_tx_hash)
async def invalid_tx_message(message: Message, user):
    await message.answer(get_text("invalid_tx", user.language))

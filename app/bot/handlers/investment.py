from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select

from app.bot.keyboards.menu import main_menu
from app.bot.states import InvestmentForm
from app.database.models import Subscription, SubscriptionStatus
from app.locales import get_text

router = Router(name="investment")
UTC = timezone.utc


async def active_signal_subscription(session, user_id: int) -> Subscription | None:
    result = await session.execute(
        select(Subscription)
        .where(
            Subscription.user_id == user_id,
            Subscription.plan_key == "signal_room",
            Subscription.status == SubscriptionStatus.ACTIVE.value,
        )
        .order_by(Subscription.expires_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


def parse_investment_amount(raw: str) -> Decimal:
    cleaned = raw.strip().replace("€", "").replace("EUR", "").replace("eur", "").replace(" ", "").replace(",", ".")
    if not cleaned:
        raise InvalidOperation
    amount = Decimal(cleaned)
    if not amount.is_finite() or amount <= 0:
        raise InvalidOperation
    return amount.quantize(Decimal("0.01"))


@router.message(F.text == "💰 Investment Amount")
async def prompt_investment(message: Message, user, db_session, settings, state: FSMContext):
    subscription = await active_signal_subscription(db_session, user.id)
    if not subscription:
        await message.answer(get_text("no_subscription", user.language), reply_markup=main_menu())
        return
    await state.set_state(InvestmentForm.waiting_amount)
    await message.answer(
        get_text("investment_prompt", user.language, minimum=f"€{settings.minimum_investment_eur:,.0f}"),
        reply_markup=main_menu(),
    )


@router.message(InvestmentForm.waiting_amount, F.text)
async def submit_investment(message: Message, user, db_session, settings, bot, state: FSMContext):
    try:
        amount = parse_investment_amount(message.text)
    except InvalidOperation:
        await message.answer(get_text("investment_invalid", user.language))
        return
    minimum = Decimal(str(settings.minimum_investment_eur))
    if amount < minimum:
        await message.answer(get_text("investment_too_low", user.language, minimum=f"€{minimum:,.2f}"))
        return
    subscription = await active_signal_subscription(db_session, user.id)
    if not subscription:
        await state.clear()
        await message.answer(get_text("no_subscription", user.language), reply_markup=main_menu())
        return
    user.preferred_investment_amount = amount
    user.investment_submitted_at = datetime.now(UTC)
    await db_session.commit()
    username = f"@{user.username}" if user.username else "—"
    admin_text = get_text(
        "investment_admin_notification",
        "en",
        name=user.first_name or "Unknown",
        username=username,
        telegram_id=user.telegram_id,
        plan=f"${settings.signal_room_price:.0f} Signal Room",
        amount=f"€{amount:,.2f}",
    )
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(admin_id, admin_text)
        except Exception:
            continue
    await state.clear()
    await message.answer(get_text("investment_noted", user.language, amount=f"€{amount:,.2f}"), reply_markup=main_menu())
    await message.answer(
        get_text("investment_next_step", user.language, contact=settings.admin_contact, vip=settings.vip_channel_link),
        reply_markup=main_menu(),
    )
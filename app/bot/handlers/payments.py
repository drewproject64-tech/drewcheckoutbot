from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.bot.keyboards.admin import payment_review_keyboard
from app.bot.keyboards.menu import main_menu
from app.bot.keyboards.plans import wallet_keyboard
from app.bot.states import InvestmentForm, PaymentForm
from app.database.models import Payment, PaymentStatus, Subscription, SubscriptionStatus
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
    await callback.message.answer(get_text("payment_instructions", user.language, plan=plan["name"], amount=float(plan["price"]), network=settings.payment_network, wallet=settings.usdt_wallet), reply_markup=wallet_keyboard(settings.usdt_wallet))
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
    payment = Payment(user_id=user.id, plan_key=plan_key, amount=Decimal(str(float(plan["price"]))), currency="USDT", network=settings.payment_network, wallet_address=settings.usdt_wallet, screenshot_file_id=screenshot_file_id, transaction_hash=tx_hash, status=PaymentStatus.PENDING.value)
    db_session.add(payment)
    try:
        await db_session.flush()
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        await message.answer(get_text("duplicate_tx", user.language))
        return
    username = f"@{user.username}" if user.username else "—"
    caption = ("💳 New Payment Pending\n\n" f"Payment ID: #{payment.id}\n" f"User: {user.first_name or 'Unknown'}\n" f"Username: {username}\n" f"Telegram ID: {user.telegram_id}\n\n" f"Plan: {plan['name']}\n" f"Amount: ${float(plan['price']):.2f} USDT\n" f"Network: {settings.payment_network}\n\n" f"Transaction hash:\n{tx_hash}")
    for admin_id in settings.admin_ids:
        try:
            await bot.send_photo(admin_id, payment.screenshot_file_id, caption=caption, reply_markup=payment_review_keyboard(payment.id))
        except Exception:
            continue
    await state.clear()
    await message.answer(get_text("payment_submitted", user.language, payment_id=payment.id), reply_markup=main_menu())

@router.message(PaymentForm.waiting_tx_hash)
async def invalid_tx_message(message: Message, user):
    await message.answer(get_text("invalid_tx", user.language))

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


_CURRENCY_SYMBOLS = {
    "€": "EUR", "$": "USD", "£": "GBP", "¥": "JPY", "₹": "INR", "₦": "NGN",
    "₽": "RUB", "₩": "KRW", "₺": "TRY", "₫": "VND", "₴": "UAH",
    "₱": "PHP", "฿": "THB", "R$": "BRL",
}

_CURRENCY_NAMES = {
    "EUR": "EUR", "EURO": "EUR", "EUROS": "EUR",
    "USD": "USD", "US DOLLAR": "USD", "US DOLLARS": "USD", "DOLLAR": "USD", "DOLLARS": "USD",
    "GBP": "GBP", "POUND": "GBP", "POUNDS": "GBP", "STERLING": "GBP",
    "JPY": "JPY", "YEN": "JPY", "INR": "INR", "RUPEE": "INR", "RUPEES": "INR",
    "NGN": "NGN", "NAIRA": "NGN", "CAD": "CAD", "AUD": "AUD", "CHF": "CHF",
    "CNY": "CNY", "RMB": "CNY", "ZAR": "ZAR", "BRL": "BRL", "MXN": "MXN",
    "SGD": "SGD", "NZD": "NZD", "AED": "AED", "SAR": "SAR", "QAR": "QAR",
    "HKD": "HKD", "SEK": "SEK", "NOK": "NOK", "DKK": "DKK", "PLN": "PLN",
    "TRY": "TRY", "KRW": "KRW", "THB": "THB", "PHP": "PHP", "VND": "VND",
    "RUB": "RUB", "UAH": "UAH",
}

_CURRENCY_CODES = set(_CURRENCY_NAMES.values())


def parse_investment_amount(raw: str) -> tuple[Decimal, str]:
    text_value = raw.strip()
    if not text_value:
        raise ValueError

    currency = None
    upper = text_value.upper()

    for symbol, code in sorted(_CURRENCY_SYMBOLS.items(), key=lambda item: len(item[0]), reverse=True):
        if symbol in text_value:
            currency = code
            text_value = text_value.replace(symbol, "")
            break

    if currency is None:
        import re
        match = re.search(r"(?<![A-Z])[A-Z]{3}(?![A-Z])", upper)
        if match and match.group(0) in _CURRENCY_CODES:
            currency = match.group(0)
            text_value = upper.replace(currency, "")

    if currency is None:
        for name, code in sorted(_CURRENCY_NAMES.items(), key=lambda item: len(item[0]), reverse=True):
            if name in upper:
                currency = code
                text_value = upper.replace(name, "")
                break

    if currency is None:
        currency = "EUR"

    numeric = text_value.strip().replace(" ", "").replace("'", "")
    if not numeric:
        raise ValueError

    if "," in numeric and "." in numeric:
        if numeric.rfind(",") > numeric.rfind("."):
            numeric = numeric.replace(".", "").replace(",", ".")
        else:
            numeric = numeric.replace(",", "")
    elif "," in numeric:
        parts = numeric.split(",")
        numeric = "".join(parts[:-1]) + "." + parts[-1] if len(parts[-1]) != 3 else "".join(parts)
    elif "." in numeric:
        parts = numeric.split(".")
        numeric = "".join(parts[:-1]) + "." + parts[-1] if len(parts[-1]) != 3 else "".join(parts)

    if not numeric.replace(".", "", 1).isdigit():
        raise ValueError

    amount = Decimal(numeric)
    if not amount.is_finite() or amount <= 0:
        raise ValueError
    return amount.quantize(Decimal("0.01")), currency


def format_money(amount: Decimal, currency: str) -> str:
    symbols = {v: k for k, v in _CURRENCY_SYMBOLS.items()}
    symbol = symbols.get(currency)
    return f"{symbol}{amount:,.2f}" if symbol else f"{amount:,.2f} {currency}"


@router.message(F.text)
async def submit_investment_amount(message: Message, user, db_session, settings, bot, state: FSMContext):
    if not user.investment_pending:
        return

    try:
        amount, currency = parse_investment_amount(message.text)
    except (ValueError, ArithmeticError):
        await message.answer(
            get_text(
                "investment_invalid",
                user.language,
                example="$1,000, €1,000, £1,000, or 1,000 USD",
            )
        )
        return

    minimum = Decimal(str(settings.minimum_investment_eur))
    if amount < minimum:
        await message.answer(
            get_text("investment_too_low", user.language, minimum=f"{minimum:,.0f}")
        )
        return

    subscription = await active_signal_subscription(db_session, user.id)
    if not subscription:
        user.investment_pending = False
        await db_session.commit()
        await message.answer(get_text("no_subscription", user.language), reply_markup=main_menu())
        return

    user.preferred_investment_amount = amount
    user.preferred_investment_currency = currency
    user.investment_submitted_at = datetime.now(timezone.utc)
    user.investment_pending = False
    await db_session.commit()

    username = f"@{user.username}" if user.username else "—"
    formatted_amount = format_money(amount, currency)
    admin_text = get_text(
        "investment_admin_notification",
        "en",
        name=user.first_name or "Unknown",
        username=username,
        telegram_id=user.telegram_id,
        plan="{} Signal Room".format(settings.signal_room_price),
        amount=formatted_amount,
    )
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(admin_id, admin_text)
        except Exception:
            continue

    await state.clear()
    await message.answer(
        get_text("investment_noted", user.language, amount=formatted_amount),
        reply_markup=main_menu(),
    )
    await message.answer(
        get_text(
            "investment_next_step",
            user.language,
            contact=settings.admin_contact,
            vip=settings.vip_channel_link,
        ),
        reply_markup=main_menu(),
    )

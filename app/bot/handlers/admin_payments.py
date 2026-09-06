from __future__ import annotations

from datetime import datetime, timezone

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.bot.states import RejectionForm
from app.database.models import Payment, PaymentStatus, User
from app.locales import get_text
from app.services.subscription_service import activate_subscription, plan_name

router = Router(name="admin_payments")
UTC = timezone.utc


def is_admin(user_id: int, settings) -> bool:
    return user_id in settings.admin_ids


async def load_payment(session, payment_id: int) -> Payment | None:
    result = await session.execute(select(Payment).where(Payment.id == payment_id))
    return result.scalar_one_or_none()


async def is_vip_member(bot, channel_id, telegram_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=telegram_id)
        return member.status in {"creator", "administrator", "member"} or (
            member.status == "restricted" and getattr(member, "is_member", False)
        )
    except Exception:
        return False


@router.callback_query(F.data.startswith("approve_payment:"))
async def approve_payment(callback: CallbackQuery, user, settings, db_session, bot):
    if not is_admin(callback.from_user.id, settings):
        await callback.answer(get_text("unauthorized", user.language), show_alert=True)
        return

    try:
        payment_id = int(callback.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await callback.answer("Invalid payment", show_alert=True)
        return

    payment = await load_payment(db_session, payment_id)
    if payment is None:
        await callback.answer("Payment not found", show_alert=True)
        return
    if payment.status != PaymentStatus.PENDING.value:
        await callback.answer(f"Already {payment.status}", show_alert=True)
        return

    result = await db_session.execute(select(User).where(User.id == payment.user_id))
    customer = result.scalar_one_or_none()
    if customer is None:
        await callback.answer("Customer not found", show_alert=True)
        return

    if not await is_vip_member(bot, settings.vip_channel_id, customer.telegram_id):
        await callback.answer("User has not joined the VIP channel. Subscription not activated.", show_alert=True)
        await bot.send_message(
            customer.telegram_id,
            "⚠️ Your payment is waiting for VIP access verification.\n\n"
            f"Join the VIP channel first:\n{settings.vip_channel_link}\n\n"
            f"After joining, contact the admin: {settings.admin_contact}\n\n"
            "Your subscription will not start until you have joined the channel.",
        )
        return

    payment.status = PaymentStatus.APPROVED.value
    payment.admin_id = callback.from_user.id
    payment.reviewed_at = datetime.now(UTC)
    subscription = await activate_subscription(db_session, payment, customer, settings)
    await db_session.commit()

    if callback.message.photo:
        await callback.message.edit_caption(caption=get_text("approved_admin", "en", payment_id=payment.id, admin_id=callback.from_user.id), reply_markup=None)
    else:
        await callback.message.edit_text(get_text("approved_admin", "en", payment_id=payment.id, admin_id=callback.from_user.id), reply_markup=None)

    await bot.send_message(customer.telegram_id, get_text("approval", customer.language, channel=settings.vip_channel_link, contact=settings.admin_contact, plan=plan_name(settings, subscription.plan_key), expires=subscription.expires_at.strftime("%Y-%m-%d %H:%M UTC"), grace=subscription.grace_until.strftime("%Y-%m-%d %H:%M UTC")))
    await callback.answer("Approved")


@router.callback_query(F.data.startswith("reject_payment:"))
async def reject_payment(callback: CallbackQuery, state: FSMContext, user, settings, db_session):
    if not is_admin(callback.from_user.id, settings):
        await callback.answer(get_text("unauthorized", user.language), show_alert=True)
        return
    try:
        payment_id = int(callback.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await callback.answer("Invalid payment", show_alert=True)
        return
    payment = await load_payment(db_session, payment_id)
    if payment is None or payment.status != PaymentStatus.PENDING.value:
        await callback.answer("Payment is no longer pending", show_alert=True)
        return
    await state.set_state(RejectionForm.waiting_reason)
    await state.update_data(payment_id=payment_id, admin_id=callback.from_user.id)
    await callback.message.answer("Send the rejection reason for payment #" + str(payment_id) + ".")
    await callback.answer()


@router.message(RejectionForm.waiting_reason, F.text)
async def submit_rejection_reason(message: Message, state: FSMContext, settings, db_session, bot):
    if not is_admin(message.from_user.id, settings):
        await state.clear()
        return
    reason = message.text.strip()[:1000]
    if not reason:
        await message.answer("Please send a rejection reason.")
        return
    data = await state.get_data()
    try:
        payment_id = int(data["payment_id"])
    except (KeyError, ValueError):
        await state.clear()
        await message.answer("Payment context expired. Please review the payment again.")
        return
    payment = await load_payment(db_session, payment_id)
    if payment is None or payment.status != PaymentStatus.PENDING.value:
        await state.clear()
        await message.answer("Payment is no longer pending.")
        return
    result = await db_session.execute(select(User).where(User.id == payment.user_id))
    customer = result.scalar_one_or_none()
    payment.status = PaymentStatus.REJECTED.value
    payment.admin_id = message.from_user.id
    payment.admin_note = reason
    payment.reviewed_at = datetime.now(UTC)
    await db_session.commit()
    if customer:
        await bot.send_message(customer.telegram_id, get_text("rejection", customer.language, reason=reason))
    await message.answer(get_text("rejected_admin", "en", payment_id=payment_id, admin_id=message.from_user.id))
    await state.clear()

from __future__ import annotations

from decimal import Decimal

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import func, select

from app.database.models import Payment, PaymentStatus, Subscription, SubscriptionStatus, User

router = Router(name="admin_stats")


def is_admin(user_id: int, settings) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("admin_stats"))
async def admin_stats(message: Message, settings, db_session):
    if not is_admin(message.from_user.id, settings):
        return

    active_result = await db_session.execute(
        select(func.count(Subscription.id)).where(
            Subscription.status == SubscriptionStatus.ACTIVE.value
        )
    )
    active_subscribers = int(active_result.scalar() or 0)

    grace_result = await db_session.execute(
        select(func.count(Subscription.id)).where(
            Subscription.status == SubscriptionStatus.GRACE.value
        )
    )
    grace_subscribers = int(grace_result.scalar() or 0)

    revenue_result = await db_session.execute(
        select(func.coalesce(func.sum(Payment.amount), 0)).where(
            Payment.status == PaymentStatus.APPROVED.value
        )
    )
    total_revenue = Decimal(str(revenue_result.scalar() or 0))

    payments_result = await db_session.execute(
        select(func.count(Payment.id)).where(
            Payment.status == PaymentStatus.APPROVED.value
        )
    )
    approved_payments = int(payments_result.scalar() or 0)

    users_result = await db_session.execute(select(func.count(User.id)))
    total_users = int(users_result.scalar() or 0)

    await message.answer(
        "📊 <b>Drew FX Admin Statistics</b>\n\n"
        f"👥 Active subscribers: <b>{active_subscribers}</b>\n"
        f"⏳ Grace-period subscribers: <b>{grace_subscribers}</b>\n"
        f"💰 Total approved revenue: <b>{total_revenue:.2f} USDT</b>\n"
        f"✅ Approved payments: <b>{approved_payments}</b>\n"
        f"🧑‍💻 Total registered users: <b>{total_users}</b>\n\n"
        "Use this report to track subscriber growth, retained grace-period users, and total bot revenue."
    )

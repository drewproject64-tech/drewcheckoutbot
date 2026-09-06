from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.database.models import Payment, PaymentStatus, Subscription, SubscriptionStatus, User
from app.locales import get_text

UTC = timezone.utc


def plan_name(settings: Settings, plan_key: str) -> str:
    plan = settings.plans.get(plan_key)
    return str(plan["name"]) if plan else plan_key


async def get_current_subscription(session: AsyncSession, user_id: int) -> Subscription | None:
    result = await session.execute(
        select(Subscription)
        .where(Subscription.user_id == user_id, Subscription.status.in_([
            SubscriptionStatus.ACTIVE.value, SubscriptionStatus.GRACE.value
        ]))
        .order_by(Subscription.expires_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def activate_subscription(
    session: AsyncSession,
    payment: Payment,
    user: User,
    settings: Settings,
    now: datetime | None = None,
) -> Subscription:
    now = (now or datetime.now(UTC)).astimezone(UTC)
    existing = await get_current_subscription(session, user.id)

    if existing and existing.status != SubscriptionStatus.CANCELLED.value and existing.expires_at > now:
        started_at = existing.started_at
        expires_at = existing.expires_at + timedelta(days=settings.subscription_days)
        existing.plan_key = payment.plan_key
        existing.payment_id = payment.id
        existing.status = SubscriptionStatus.ACTIVE.value
        existing.expires_at = expires_at
        existing.grace_until = expires_at + timedelta(days=settings.grace_period_days)
        existing.last_reminder_sent_at = None
        subscription = existing
    else:
        started_at = now
        expires_at = now + timedelta(days=settings.subscription_days)
        subscription = Subscription(
            user_id=user.id,
            plan_key=payment.plan_key,
            payment_id=payment.id,
            status=SubscriptionStatus.ACTIVE.value,
            started_at=started_at,
            expires_at=expires_at,
            grace_until=expires_at + timedelta(days=settings.grace_period_days),
        )
        session.add(subscription)

    await session.flush()
    return subscription


async def format_subscription_status(session: AsyncSession, user: User, settings: Settings) -> str:
    subscription = await get_current_subscription(session, user.id)
    now = datetime.now(UTC)
    if not subscription:
        return get_text("no_subscription", user.language)

    if subscription.status == SubscriptionStatus.ACTIVE.value and now >= subscription.expires_at:
        status = "Grace period"
    elif subscription.status == SubscriptionStatus.GRACE.value:
        status = "Grace period"
    elif subscription.status == SubscriptionStatus.EXPIRED.value:
        status = "Expired"
    else:
        status = "Active"

    if now < subscription.expires_at:
        days = max(0, (subscription.expires_at - now).days)
    elif now < subscription.grace_until:
        days = max(0, (subscription.grace_until - now).days)
    else:
        days = 0

    return get_text(
        "subscription", user.language,
        plan=plan_name(settings, subscription.plan_key),
        status=status,
        expires=subscription.expires_at.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC"),
        grace=subscription.grace_until.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC"),
        days=days,
    )

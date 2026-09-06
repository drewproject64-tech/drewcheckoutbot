from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Payment, PaymentStatus, Subscription, SubscriptionStatus, User


async def upsert_user(session: AsyncSession, telegram_user) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_user.id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(telegram_id=telegram_user.id, username=telegram_user.username, first_name=telegram_user.first_name)
        session.add(user)
    else:
        user.username = telegram_user.username
        user.first_name = telegram_user.first_name
    await session.flush()
    return user


async def get_subscription(session: AsyncSession, user_id: int) -> Subscription | None:
    result = await session.execute(
        select(Subscription).where(Subscription.user_id == user_id).order_by(desc(Subscription.created_at)).limit(1)
    )
    return result.scalar_one_or_none()


async def tx_hash_exists(session: AsyncSession, tx_hash: str) -> bool:
    result = await session.execute(select(Payment.id).where(Payment.transaction_hash == tx_hash).limit(1))
    return result.scalar_one_or_none() is not None

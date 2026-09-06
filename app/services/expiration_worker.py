from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging

from aiogram import Bot
from sqlalchemy import select

from app.config import Settings
from app.database.models import Subscription, SubscriptionStatus, User
from app.locales import get_text
from app.services.channel_service import normalize_chat_id, remove_from_vip
from app.services.subscription_service import plan_name

logger = logging.getLogger(__name__)
UTC = timezone.utc


async def process_subscriptions(bot: Bot, db, settings: Settings) -> None:
    now = datetime.now(UTC)
    reminder_cutoff = now + timedelta(days=settings.reminder_days_before_expiry)

    async with db.session_factory() as session:
        result = await session.execute(
            select(Subscription, User)
            .join(User, User.id == Subscription.user_id)
            .where(Subscription.status.in_([
                SubscriptionStatus.ACTIVE.value,
                SubscriptionStatus.GRACE.value,
            ]))
        )
        rows = result.all()

        for subscription, user in rows:
            try:
                if subscription.status == SubscriptionStatus.ACTIVE.value and now < subscription.expires_at <= reminder_cutoff:
                    if subscription.last_reminder_sent_at is None:
                        days = max(1, (subscription.expires_at - now).days)
                        await bot.send_message(user.telegram_id, get_text("renewal", user.language, days=days))
                        subscription.last_reminder_sent_at = now

                if subscription.status == SubscriptionStatus.ACTIVE.value and now >= subscription.expires_at:
                    subscription.status = SubscriptionStatus.GRACE.value
                    await bot.send_message(user.telegram_id, get_text("grace", user.language, days=settings.grace_period_days))

                if subscription.status == SubscriptionStatus.GRACE.value and now >= subscription.grace_until:
                    removed = await remove_from_vip(bot, normalize_chat_id(settings.vip_channel_username), user.telegram_id)
                    subscription.status = SubscriptionStatus.EXPIRED.value
                    if removed:
                        await bot.send_message(user.telegram_id, get_text("removed", user.language))
                    else:
                        logger.info("Marked user %s expired; Telegram removal was unsuccessful", user.telegram_id)
            except Exception:
                logger.exception("Subscription processing failed for subscription %s", subscription.id)
                continue

        await session.commit()

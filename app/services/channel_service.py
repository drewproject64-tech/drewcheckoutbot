from __future__ import annotations

import logging
from urllib.parse import urlparse

from aiogram import Bot

logger = logging.getLogger(__name__)


def normalize_chat_id(username: str) -> str:
    username = username.strip()
    if username.startswith("https://t.me/"):
        return "@" + username.rstrip("/").split("/")[-1]
    return username if username.startswith("@") else "@" + username


async def remove_from_vip(bot: Bot, chat_id: str, telegram_user_id: int) -> bool:
    try:
        await bot.ban_chat_member(chat_id=chat_id, user_id=telegram_user_id, revoke_messages=False)
        await bot.unban_chat_member(chat_id=chat_id, user_id=telegram_user_id, only_if_banned=True)
        return True
    except Exception as exc:
        logger.warning("Unable to remove Telegram user %s from %s: %s", telegram_user_id, chat_id, exc)
        return False

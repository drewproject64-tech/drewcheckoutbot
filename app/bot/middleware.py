from __future__ import annotations

from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable

from app.database.repositories import upsert_user


class DbUserMiddleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        if getattr(event, "from_user", None) is None:
            return await handler(event, data)
        async with self.db.session_factory() as session:
            user = await upsert_user(session, event.from_user)
            await session.commit()
        data["user"] = user
        return await handler(event, data)

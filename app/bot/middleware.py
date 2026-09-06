from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware

from app.database.repositories import upsert_user


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, db, settings):
        self.db = db
        self.settings = settings

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        async with self.db.session_factory() as session:
            data["db_session"] = session
            data["settings"] = self.settings
            if getattr(event, "from_user", None) is not None:
                data["user"] = await upsert_user(session, event.from_user)
                await session.commit()
            try:
                return await handler(event, data)
            except Exception:
                await session.rollback()
                raise

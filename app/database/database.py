from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings
from app.database.models import Base


class Database:
    def __init__(self, settings: Settings) -> None:
        self.engine = create_async_engine(settings.database_url, pool_pre_ping=True)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def init(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

            # create_all() does not alter existing tables. These idempotent
            # PostgreSQL migrations keep existing production databases in sync
            # with the User model without deleting any existing data.
            await conn.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN IF NOT EXISTS preferred_investment_amount NUMERIC(12, 2)"
                )
            )
            await conn.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN IF NOT EXISTS investment_submitted_at TIMESTAMPTZ"
                )
            )

    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            yield session

    async def close(self) -> None:
        await self.engine.dispose()

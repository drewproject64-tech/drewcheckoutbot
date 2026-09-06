from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _parse_admin_ids(raw: str) -> set[int]:
    values: set[int] = set()
    for item in raw.split(","):
        item = item.strip()
        if item:
            values.add(int(item))
    if not values:
        raise RuntimeError("ADMIN_IDS must contain at least one Telegram ID")
    return values


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return "postgresql+asyncpg://" + url[len("postgres://") :]
    if url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url[len("postgresql://") :]
    return url


@dataclass(frozen=True)
class Settings:
    bot_token: str
    database_url: str
    admin_ids: set[int]
    vip_channel_link: str
    vip_channel_username: str
    admin_contact: str
    usdt_wallet: str
    payment_network: str
    signal_room_price: float
    all_access_price: float
    subscription_days: int
    grace_period_days: int
    reminder_days_before_expiry: int
    timezone: str
    log_level: str

    @property
    def plans(self) -> dict[str, dict[str, object]]:
        return {
            "signal_room": {
                "name": "Signal Room",
                "price": self.signal_room_price,
                "access": "Drew FX Signal Room",
            },
            "all_access": {
                "name": "All Access",
                "price": self.all_access_price,
                "access": "VIP access plus advanced benefits",
            },
        }


def load_settings() -> Settings:
    return Settings(
        bot_token=_required("BOT_TOKEN"),
        database_url=normalize_database_url(_required("DATABASE_URL")),
        admin_ids=_parse_admin_ids(_required("ADMIN_IDS")),
        vip_channel_link=_required("VIP_CHANNEL_LINK"),
        vip_channel_username=os.getenv("VIP_CHANNEL_USERNAME", "DREWVIPFX").strip(),
        admin_contact=_required("ADMIN_CONTACT"),
        usdt_wallet=_required("USDT_WALLET"),
        payment_network=os.getenv("PAYMENT_NETWORK", "TRC20").strip().upper(),
        signal_room_price=float(os.getenv("SIGNAL_ROOM_PRICE", "70")),
        all_access_price=float(os.getenv("ALL_ACCESS_PRICE", "100")),
        subscription_days=int(os.getenv("SUBSCRIPTION_DAYS", "30")),
        grace_period_days=int(os.getenv("GRACE_PERIOD_DAYS", "3")),
        reminder_days_before_expiry=int(os.getenv("REMINDER_DAYS_BEFORE_EXPIRY", "3")),
        timezone=os.getenv("TIMEZONE", "UTC").strip(),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
    )

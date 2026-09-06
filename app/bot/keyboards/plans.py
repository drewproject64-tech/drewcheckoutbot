from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup


def plans_keyboard(plans: dict[str, dict[str, object]]) -> InlineKeyboardMarkup:
    rows = []
    for key, plan in plans.items():
        rows.append([
            InlineKeyboardButton(
                text=f"⭐ {plan['name']} — ${float(plan['price']):.0f} USDT",
                callback_data=f"plan:{key}",
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def wallet_keyboard(wallet: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Copy USDT Address", copy_text=CopyTextButton(text=wallet))],
        ]
    )

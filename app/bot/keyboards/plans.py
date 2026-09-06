from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def plans_keyboard(plans: dict[str, dict[str, object]]) -> InlineKeyboardMarkup:
    rows = []
    for key, plan in plans.items():
        rows.append([InlineKeyboardButton(text=f"⭐ {plan['name']} — ${float(plan['price']):.0f} USDT", callback_data=f"plan:{key}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

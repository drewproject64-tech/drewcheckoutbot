from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def payment_review_keyboard(payment_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Approve", callback_data=f"approve_payment:{payment_id}")],
        [InlineKeyboardButton(text="❌ Reject", callback_data=f"reject_payment:{payment_id}")],
    ])

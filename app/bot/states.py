from aiogram.fsm.state import State, StatesGroup


class PaymentForm(StatesGroup):
    waiting_screenshot = State()
    waiting_tx_hash = State()


class RejectionForm(StatesGroup):
    waiting_reason = State()

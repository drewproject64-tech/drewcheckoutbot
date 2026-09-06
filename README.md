# Drew FX Checkout Bot

Production-oriented Telegram subscription payment bot for Drew FX VIP.

## Features

- English, Italian, French, and German UI
- Persistent reply-keyboard main menu
- Signal Room and All Access plans
- USDT/TRC20 payment instructions
- Payment screenshot + transaction-hash submission
- Multi-admin approval/rejection workflow
- PostgreSQL persistence with SQLAlchemy async
- Subscription expiry and 3-day grace-period processing
- VIP removal after grace period
- Render background-worker deployment

## Local setup

1. Create a Python 3.12 environment.
2. Install `requirements.txt`.
3. Copy `.env.example` to `.env` and fill in real values.
4. Ensure the bot is an administrator of the VIP channel with membership-management permissions.
5. Start with `python -m app.main`.

Do not commit `.env` or bot credentials.

## Important configuration

Verify the final USDT wallet address before accepting payments. The repository intentionally uses a placeholder in `.env.example` so an unverified address is not accidentally deployed.

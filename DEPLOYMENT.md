# Deployment Guide

## 1. Render PostgreSQL

Create a Render PostgreSQL database and copy its **Internal Database URL**.

## 2. Render Background Worker

Create a Background Worker connected to:

`drewproject64-tech/drewcheckoutbot`

Use the included `render.yaml`, or configure:

- Build: `pip install -r requirements.txt`
- Start: `python -m app.main`

## 3. Environment variables

Set every variable from `.env.example` in Render. Use the real bot token, database URL, administrator IDs, channel configuration, admin contact, and a **verified** USDT TRC20 wallet.

The database URL may be supplied by Render as `postgres://` or `postgresql://`; the application normalizes it to `postgresql+asyncpg://` automatically.

## 4. Telegram configuration

Add the bot as an administrator in the VIP channel. Grant the permissions required to manage membership. Confirm the bot token and administrator Telegram IDs.

For removal to work, `VIP_CHANNEL_USERNAME` must identify the actual channel username (for example `DREWVIPFX`) or be otherwise adapted to a channel identifier supported by the deployment.

## 5. Production checks

Confirm:

- `/start` and language selection work.
- Every visible main-menu button responds.
- Both plans display the correct server-side price.
- Screenshot and transaction-hash submission create a pending payment.
- Admins receive the payment proof.
- Approve creates/extends one subscription.
- Reject records a reason and notifies the customer.
- Scheduler reminders and grace processing run.
- VIP removal works with the bot's Telegram permissions.
- Logs contain no secrets.

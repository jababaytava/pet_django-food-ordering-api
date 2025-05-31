import logging
import os
import requests

logger = logging.getLogger("telegram_logger")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_message(message: str, order_id: int):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "Confirmed", "callback_data": f"/confirmed_{order_id}"},
                    {"text": "Canceled", "callback_data": f"/canceled_{order_id}"},
                    {"text": "Completed", "callback_data": f"/completed_{order_id}"},
                ]
            ]
        },
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Telegram error: {e}")

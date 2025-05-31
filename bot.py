import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes

BACKEND_URL = os.getenv("BACKEND_URL")
SECRET = os.getenv("TELEGRAM_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback_data = update.callback_query.data

    if callback_data.startswith("/confirmed_"):
        order_id = callback_data.split("_")[1]
        new_status = "confirmed"
    elif callback_data.startswith("/canceled_"):
        order_id = callback_data.split("_")[1]
        new_status = "canceled"
    elif callback_data.startswith("/completed_"):
        order_id = callback_data.split("_")[1]
        new_status = "completed"
    else:
        await update.callback_query.answer("Unknown action.")
        return

    response = requests.post(
        f"{BACKEND_URL}/api/orders/update-status/",
        json={"order_id": order_id, "status": new_status, "secret": SECRET},
    )

    if response.ok:
        await update.callback_query.answer(f"Status updated: {new_status}")
    else:
        await update.callback_query.answer("Update failed")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("Telegram Bot started")
    app.run_polling()

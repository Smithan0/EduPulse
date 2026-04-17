"""Entry point and configuration for the EduPulse Telegram bot."""
from __future__ import annotations

import logging
import os
from typing import Optional

from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from src.core.db import init_db
from src.handlers.telegram import handle_message
from src.handlers.gemini import GeminioClient

LOGGER = logging.getLogger("edupulse")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def build_application(token: str, webhook_url: Optional[str]) -> Application:
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    if webhook_url:
        application.post_init = lambda _: application.bot.set_webhook(webhook_url)

    return application


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to EduPulse. Send me a topic you'd like to explore.")


def main() -> None:
    load_dotenv()
    configure_logging()
    init_db()

    token = os.environ["TELEGRAM_BOT_TOKEN"]
    webhook_url = os.environ.get("TELEGRAM_WEBHOOK_URL")
    gemini_key = os.environ["GOOGLE_API_KEY"]

    client = GeminioClient(gemini_key)
    application = build_application(token, webhook_url)

    if webhook_url:
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)),
            webhook_url_path="/webhook",
            webhook_url=webhook_url,
        )
    else:
        application.run_polling()


if __name__ == "__main__":
    main()

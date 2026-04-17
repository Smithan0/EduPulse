"""Telegram-specific handler wiring."""
from __future__ import annotations

from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from src.core.interaction import create_interaction, update_status
from src.handlers.gemini import GeminioClient


def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.from_user:
        return

    user_id = update.message.from_user.id
    text = update.message.text or ""

    interaction_id = create_interaction(user_id, text)
    context.user_data.setdefault("last_interaction", interaction_id)

    response = context.application.chat_data.get("gemini_client")
    if response is None:
        gem_client = GeminioClient(context.application.bot.token)
        context.application.chat_data["gemini_client"] = gem_client
    else:
        gem_client = response

    update_status(interaction_id, "processing")
    try:
        gemini_prompt = text  # placeholder for prompt builder
        gemini_response = gem_client.query(gemini_prompt)
        update_status(interaction_id, "complete", gemini_out=gemini_response, prompt_used=gemini_prompt)
        await update.message.reply_text(gemini_response)
    except Exception as exc:
        update_status(interaction_id, "failed")
        await update.message.reply_text("Sorry, I hit an error while reaching Gemini. Try again later.")

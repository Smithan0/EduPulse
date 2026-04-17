"""Gemini client abstractions."""
from __future__ import annotations

from typing import Optional

from google.generativeai import Client


class GeminioClient:
    def __init__(self, api_key: str) -> None:
        self._client = Client(api_key=api_key)

    def query(self, prompt: str) -> str:
        message = self._client.messages.create(
            model="gemini-1.5",
            prompt=prompt,
        )
        return message.result.get("content", "I’m still thinking…")

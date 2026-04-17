"""Domain objects that reflect the SQLite schema."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class UserSession:
    user_id: int
    session_ctx: Optional[str]
    updated_at: Optional[datetime]


@dataclass(frozen=True)
class InteractionRecord:
    id: int
    user_id: int
    raw_input: str
    status: str
    prompt_used: Optional[str]
    gemini_out: Optional[str]
    created_at: Optional[datetime]
    resolved_at: Optional[datetime]

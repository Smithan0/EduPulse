"""State transition helpers that mirror the FSM described in ``schema.sql``."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional

from .db import get_conn
from .models import InteractionRecord


STATUS_RECEIVED = "received"
STATUS_PROCESSING = "processing"
STATUS_COMPLETE = "complete"
STATUS_FAILED = "failed"


def create_interaction(user_id: int, raw_input: str) -> int:
    with get_conn() as conn:
        cursor = conn.execute(
            """
            INSERT INTO interactions (user_id, raw_input, status)
            VALUES (?, ?, ?)
            """,
            (user_id, raw_input, STATUS_RECEIVED),
        )
        conn.commit()
        return cursor.lastrowid


def update_status(interaction_id: int, status: str, **fields: Optional[str]) -> None:
    if not fields:
        template = "UPDATE interactions SET status = ?, resolved_at = ? WHERE id = ?"
        params = (status, datetime.utcnow(), interaction_id)
    else:
        updates = ", ".join(f"{k} = ?" for k in fields)
        template = f"UPDATE interactions SET status = ?, {updates}, resolved_at = ? WHERE id = ?"
        params = (status, *fields.values(), datetime.utcnow(), interaction_id)

    with get_conn() as conn:
        conn.execute(template, params)
        conn.commit()


def fetch_recent_for_user(user_id: int, limit: int = 5) -> Iterable[InteractionRecord]:
    with get_conn() as conn:
        cursor = conn.execute(
            """
            SELECT * FROM interactions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
        rows = cursor.fetchall()
    for row in rows:
        yield InteractionRecord(
            id=row["id"],
            user_id=row["user_id"],
            raw_input=row["raw_input"],
            status=row["status"],
            prompt_used=row["prompt_used"],
            gemini_out=row["gemini_out"],
            created_at=row["created_at"],
            resolved_at=row["resolved_at"],
        )

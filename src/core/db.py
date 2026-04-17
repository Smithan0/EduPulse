"""Persistence helpers that mirror ``schema.sql``."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from textwrap import dedent

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
SCHEMA_PATH = BASE_DIR / "schema.sql"
DB_PATH = DATA_DIR / "edupulse.db"


DEFAULT_SCHEMA = dedent("""
    PRAGMA journal_mode=WAL;

    CREATE TABLE IF NOT EXISTS users (
        user_id     INTEGER PRIMARY KEY,
        session_ctx TEXT,
        updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS interactions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL REFERENCES users(user_id),
        raw_input   TEXT    NOT NULL,
        status      TEXT    NOT NULL DEFAULT 'received',
        prompt_used TEXT,
        gemini_out  TEXT,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
        resolved_at DATETIME
    );

    CREATE INDEX IF NOT EXISTS idx_interactions_status
        ON interactions(status);

    CREATE INDEX IF NOT EXISTS idx_interactions_user
        ON interactions(user_id, created_at DESC);
""")


def ensure_data_dir() -> None:
    """Make sure the ``data/`` folder exists before we open the database."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _configure_connection(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")


def get_conn() -> sqlite3.Connection:
    """Return a new SQLite connection with the expected PRAGMA state."""
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    _configure_connection(conn)
    return conn


def init_db() -> None:
    """Create the schema if it is missing."""
    schema_text = SCHEMA_PATH.read_text() if SCHEMA_PATH.exists() else DEFAULT_SCHEMA
    with get_conn() as conn:
        conn.executescript(schema_text)
        conn.commit()

-- EduPulse — src/schema.sql
-- Source of truth for database structure.
-- Run via: sqlite3 data/edupulse.db < src/schema.sql
-- Or via:  python -c "from src.core.db import init_db; init_db()"
--
-- PRAGMA NOTES:
--   journal_mode=WAL  : persists after first SET — safe to put here
--   foreign_keys=ON   : does NOT persist across connections in SQLite
--                       Set per-connection inside db.py get_conn(), NOT here.

PRAGMA journal_mode=WAL;

-- ─────────────────────────────────────────────
-- Users
-- Stores session context between Render spin-downs.
-- session_ctx: JSON blob, truncated to 800 chars by logic.py
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    session_ctx TEXT,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────────
-- Interactions
-- Every message received is written here FIRST, before any processing.
-- Status FSM: received → processing → complete
--                                   → failed
--
-- status values:
--   received   : raw input saved, Gemini not yet called
--   processing : Gemini call in flight
--   complete   : gemini_out written, user replied
--   failed     : Gemini error OR dangling row recovered on restart
--
-- prompt_used: exact string sent to Gemini — required for benchmark
--              reproducibility. Without this, runs are not comparable.
-- ─────────────────────────────────────────────
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

-- Index: crash recovery query
--   SELECT * FROM interactions WHERE status IN ('received','processing')
CREATE INDEX IF NOT EXISTS idx_interactions_status
    ON interactions(status);

-- Index: per-user history lookup
--   SELECT * FROM interactions WHERE user_id = ? ORDER BY created_at DESC
CREATE INDEX IF NOT EXISTS idx_interactions_user
    ON interactions(user_id, created_at DESC);

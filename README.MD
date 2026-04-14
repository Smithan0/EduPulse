# EduPulse

**Type:** Telegram study bot — Gemini API + python-telegram-bot + Flask + SQLite  
**Stack:** Python · Flask · SQLite (WAL) · Render Free Tier  
**Repo:** [github.com/smithan0/edupulse](https://github.com/smithan0/edupulse)

> Structured as a **research log + working implementation**.  
> Every architectural decision is traceable to a documented experiment.  
> Code exists to generate data. Data drives decisions.

---

## Project State

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Phase              | Phase 1 — EduPulse                                                       |
| Latest Tag         | `exp00-v0.1-scaffold`                                                    |
| Deployment         | Render Free Tier (webhook mode)                                          |
| Local Dev          | Termux · Android 7 · Python 3.x                                         |
| Open Experiment    | exp01 — Webhook vs Polling latency                                       |
| SQLite Persistence | **Known limitation** — ephemeral disk on Render. Planned migration to DigitalOcean Droplet at Phase 3 using GitHub Student Pack $200 credit. |

---

## Architecture

```
PRODUCTION — Render Free Tier
══════════════════════════════════════════════════════════════

              Telegram Servers
                    │
               POST /webhook
                    │
                    ▼
        ┌───────────────────────┐
        │      src/bot.py       │
        │   Flask Listener      │
        │                       │
        │  POST /webhook ───────┼──► handlers/study.py
        │  GET  /health  ◄──────┼─── UptimeRobot (ping every 5 min)
        └───────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   handlers/study.py   │
        │                       │
        │  Step 1: write raw    │ ← IMMEDIATE — before any processing
        │  Step 2: → processing │
        │  Step 3: call Gemini  │
        │  Step 4: write result │
        │  Step 5: reply user   │
        └──────┬──────────┬─────┘
               │          │
               ▼          ▼
        core/db.py    core/gemini_client.py
        (WAL mode)    (gemini-1.5-flash)
               │
               ▼
        data/edupulse.db
        ├── interactions   status: received→processing→complete/failed
        └── users          session_ctx: JSON blob, max 800 chars


LOCAL DEV — Termux · Android 7
══════════════════════════════════════════════════════════════

./start.sh
  ├── termux-wake-lock          prevents Android background kill
  ├── source .env               API keys loaded once — no mid-session browser
  └── python src/bot.py         polling mode locally, same handlers as prod
              │
              └── core/db.py · core/logic.py · core/gemini_client.py
                  data/edupulse.db  (same schema, same write-first pattern)
```

---

## Directory Structure

```
edupulse/
├── .env.example                    required env vars, never commit .env
├── .gitignore                      python + .env + data/*.db + __pycache__
├── start.sh                        Termux dev session launcher
├── requirements.txt
├── README.md
│
├── data/
│   └── .gitkeep                    directory tracked; edupulse.db gitignored
│
├── experiments/
│   ├── methodology_01.md           exp01: webhook vs polling (active)
│   └── logs/
│       └── .gitkeep                run_NNN.json files land here
│
├── src/
│   ├── bot.py                      entry point: Flask webhook listener + startup
│   ├── schema.sql                  single source of truth for DB structure
│   ├── benchmark.py                measurement script → experiments/logs/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── db.py                   connection manager, init_db, crash recovery
│   │   ├── logic.py                pure functions only, no I/O, no side effects
│   │   └── gemini_client.py        Gemini API wrapper, sync-safe
│   └── handlers/
│       ├── __init__.py
│       └── study.py                write-first handler, atomic state transitions
│
└── tests/
    └── prompts/
        ├── syllabus_short.txt      fixed input — benchmark control variable
        └── quiz_request.txt        fixed input — benchmark variant
```

---

## Setup

```bash
# 1. Clone
git clone https://github.com/smithan0/edupulse && cd edupulse

# 2. Install (Termux — use flag if needed)
pip install -r requirements.txt
# or: pip install -r requirements.txt --break-system-packages

# 3. Configure
cp .env.example .env
nano .env   # fill in your keys

# 4. Initialise DB (creates data/edupulse.db with correct schema)
python -c "
import sys; sys.path.insert(0, 'src')
from core.db import init_db
init_db()
print('DB initialised at data/edupulse.db')
"

# 5. Start local dev
chmod +x start.sh
./start.sh
```

---

## Running Benchmarks

```bash
python src/benchmark.py --runs 3 --prompt tests/prompts/syllabus_short.txt
# Output: experiments/logs/run_001.json
# Re-run produces: run_002.json, run_003.json, etc.
```

---

## Environment Variables

See `.env.example` for full reference and descriptions.

```
TELEGRAM_BOT_TOKEN    from @BotFather
GEMINI_API_KEY        from Google AI Studio
ENVIRONMENT           development | production
WEBHOOK_URL           your Render URL (production only, no trailing slash)
```

---

## Architectural Decision Log

| Decision           | Choice                            | Rationale                                                        |
|--------------------|-----------------------------------|------------------------------------------------------------------|
| Transport          | Webhook (prod) / Polling (local)  | Render spin-down; Telegram buffers POSTs during ~10–30s cold start |
| State              | SQLite WAL, write-first           | No in-memory state survives Render spin-down                     |
| Write order        | received→processing→complete/failed | Crash recovery: restart queries `status = 'processing'`        |
| Context window     | Truncated at 800 chars            | Prevents token bloat on multi-turn sessions                      |
| Keep-alive         | UptimeRobot → GET /health         | Free; prevents idle spin-down during active use periods          |
| Local resilience   | termux-wake-lock + .env file      | Single `./start.sh` command; no browser mid-session             |
| foreign_keys       | Set per-connection in db.py       | SQLite PRAGMA foreign_keys does not persist across connections   |

Full experiment log and benchmark data: [`experiments/`](experiments/)

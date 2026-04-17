# EduPulse Architecture Roadmap

## Overview
EduPulse is a Telegram + Gemini-powered study assistant built with scalability and defensibility in mind. The architecture follows a phased rollout so each layer can be validated before adding complexity.

## Phase 0 – Foundation (complete)
- **Goal:** Establish a runnable codebase and schema-driven data layer.
- **Completed work:**
  - `src/bot.py` entrypoint (dotenv, logging, polling/webhook switch).
  - `src/core/db.py`, `models.py`, and `interaction.py` respecting `schema.sql` and exposing helpers such as `init_db()`.
  - `src/handlers/telegram.py` + `handlers/gemini.py` wiring to Gemini.
  - Inline schema fallback so the database can bootstrap even without the upstream SQL file.

## Phase 1 – Conversational workflow (next)
- **Goal:** Encode the message → Gemini → persistence loop.
- **Deliverables:**
  - Prompt builders and context tracking in `core/` (active topics, quiz states).
  - Interaction lifecycle management (`received → processing → complete/failed`).
  - Error handling + reply strategy when Gemini fails or produces ambiguous answers.
  - Tests covering each handler and FSM state.

## Phase 2 – Productization layer
- **Goal:** Layer in roadmap initiatives (AfriAlert, QuizForge, DevPortfolio).
- **Deliverables:**
  - Command router (`/learn`, `/quiz`, `/report`) backed by modular services.
  - Data exporter (CSV/JSON) for dashboards or partner apps.
  - Notification & analytics services for AfriAlert-style alerts.

## Phase 3 – Deployment & observability
- **Goal:** Harden the stack for production deployments beyond Termux.
- **Deliverables:**
  - Containerization/CI, webhook + proxy readiness, and Termux-to-cloud migrations.
  - Structured logging, retry/backoff, rate-limits, runtime metrics.
  - Security checks (webhook validity, prompt sanitization).

## Phase 4 – Extension & defensibility
- **Goal:** Build reusable IP and bridge into QuizForge/DevPortfolio.
- **Deliverables:**
  - Content versioning (prompt + response history, diff snapshots).
  - Adaptive learning pathways and analytics dashboards.
  - Public API for EduPulse data so other roadmap pieces can consume sessions.
  - Expanded test suites covering Gemini mocks, DB migrations, and CLI tooling.

Would you like a gantt-style timeline or do you want to start executing Phase 1 tasks next?  
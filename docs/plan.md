# EduPulse Implementation Plan

## Weekly roadmap
1. **Week 1 (Phase 0 wrap-up)**
   - Verify `init_db()` works with schema or defaults.
   - Flesh out `README.md` with run instructions (polling vs webhook).
   - Document the architecture in `docs/architecture.md` and link to the roadmap.
2. **Week 2 (Phase 1 part 1)**
   - Build prompt/context helpers in `src/core`.
   - Extend domain models for user sessions and quiz state.
   - Write unit tests for FSM helpers to capture the schema’s lifecycle transitions.
3. **Week 3 (Phase 1 part 2)**
   - Implement a Telegram command router and status transition executor.
   - Add a mock Gemini flow so Telegram handlers can be tested without calling the real API.
   - Validate failure paths and ensure updates set `status` and `resolved_at` correctly.
4. **Week 4 (Phase 2 part 1)**
   - Add modular command services (`/learn`, `/quiz`, `/report`).
   - Start the AfriAlert notification stub and define how alerts map to interaction records.
5. **Week 5 (Phase 2 part 2)**
   - Implement data export utilities and analytics hooks.
   - Iterate on QuizForge quiz flow, including answer validation and scoring outlines.
6. **Week 6 (Phase 3)**
   - Harden deployment: container/CI scripts, webhook readiness, logging/metrics, rate limit specs.
7. **Week 7 (Phase 4)**
   - Build content versioning, adaptive study pathways, public API endpoints, and expand test/mocking coverage.

## Dependencies & notes
- Keep schema-driven helpers (`src/core/db.py`, `interaction.py`) as the single source of truth for data lifecycle management.
- Each phase should include at least one documented decision recorded in `docs/architecture.md` (see `METHODOLOGY.MD` for the experiment process).

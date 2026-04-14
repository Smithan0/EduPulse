# EduPulse — Methodology: exp01
## Webhook vs Polling Latency on Render Free Tier

> **Rule:** One experiment per file. Do not overwrite.  
> Next experiment → `methodology_02.md`

---

## 1. Research Question

Does Render free tier's spin-down/spin-up cycle make webhook mode
measurably slower than polling for EduPulse's use case, and does
the latency difference matter to a real student user?

---

## 2. Hypothesis

> Webhook mode will have higher **cold-start** latency (~10–30 s on first
> request after idle) but lower **steady-state** latency than polling,
> because polling introduces a 1–3 s long-poll delay per cycle even
> when the instance is warm. For an active study session (messages
> every <5 min), webhook steady-state wins. For a dormant bot pinged
> once per hour, cold-start dominates and the difference is irrelevant
> to UX.

**Expected outcome:** webhook ships. Cold-start is mitigated by
UptimeRobot pinging `/health` every 5 minutes.

---

## 3. Experimental Setup

| Field             | Value                                              |
|-------------------|----------------------------------------------------|
| Control           | Polling mode — local Termux, Android 7             |
| Variant           | Webhook mode — Render Free Tier, Flask listener    |
| Bot Framework     | python-telegram-bot 20.x                           |
| Gemini Model      | gemini-1.5-flash                                   |
| Test Inputs       | `tests/prompts/syllabus_short.txt` (fixed, ~120 chars) |
| Runs per mode     | 5 minimum                                          |
| Time between runs | 30 seconds (warm instance)                         |

**Metrics collected — with units and expected ranges:**

| Metric               | Unit  | Expected (polling) | Expected (webhook) | Notes                        |
|----------------------|-------|--------------------|--------------------|------------------------------|
| `response_latency_ms`| ms    | 3000–5000          | 500–2000 (warm)    | User send → bot reply        |
| `gemini_latency_ms`  | ms    | 800–2000           | 800–2000           | API call only, mode-agnostic |
| `tokens_in`          | count | 40–80              | 40–80              | From Gemini usage_metadata   |
| `tokens_out`         | count | 80–200             | 80–200             | From Gemini usage_metadata   |
| `cold_start`         | bool  | false (local)      | true/false         | Was instance sleeping?       |

**What is NOT measured here:**
- Message loss rate (Telegram handles buffering — architectural given)
- Cost (Gemini free tier, Render free tier — no cost variable)
- Multi-user concurrency (single-user test, Phase 3 concern)

---

## 4. Results Log

_Fill this in during runs. Do not estimate. Paste from `experiments/logs/run_NNN.json`._

| Run | Tag               | Mode    | response_latency_ms | gemini_latency_ms | tokens_in | tokens_out | cold_start | Notes |
|-----|-------------------|---------|---------------------|-------------------|-----------|------------|------------|-------|
| 001 | exp01-v0.2-ctrl   | polling | —                   | —                 | —         | —          | false      | local Termux baseline |
| 002 | exp01-v0.2-ctrl   | polling | —                   | —                 | —         | —          | false      | |
| 003 | exp01-v0.2-ctrl   | polling | —                   | —                 | —         | —          | false      | |
| 004 | exp01-v0.3-var    | webhook | —                   | —                 | —         | —          | —          | Render cold start run |
| 005 | exp01-v0.3-var    | webhook | —                   | —                 | —         | —          | false      | warm instance |
| 006 | exp01-v0.3-var    | webhook | —                   | —                 | —         | —          | false      | |

---

## 5. Interpretation

_(Write this only after table is complete.)_

Answer in order:
1. Did steady-state webhook beat polling? By how much?
2. What was actual cold-start latency (not estimated)?
3. Does UptimeRobot keep-alive eliminate the cold-start problem in practice?
4. Was the hypothesis confirmed, partially confirmed, or refuted?

---

## 6. Decision

```
[ ] Webhook ships — cold-start acceptable, steady-state wins
[ ] Polling ships — latency difference too small to justify webhook complexity
[ ] Inconclusive — needs follow-up experiment (open issue #___)
```

**Commit decision with:**
```bash
git add experiments/methodology_01.md experiments/logs/
git commit -m "docs(exp01): interpretation + decision recorded"
git tag -a exp01-v1.0-closed -m "exp01: closed — [paste decision here]"
```

---

_Owner: smithan0 | Started: YYYY-MM-DD | Closed: —_

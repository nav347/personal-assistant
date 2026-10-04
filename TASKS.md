# 📋 Task Backlog

> **Workflow:**
> - **Add:** say `add task: <description>` — I append it with the next ID
> - **Pick:** say `pick a task` — I suggest the highest-priority unclaimed one
> - **Claim:** move to 🔥 Active with owner + date, commit, push (see COORDINATION.md)
> - **Done:** say `done: T-XXX` — I move it to ✅ Done with the date
> - **Drop:** say `drop: T-XXX` — moved to 🗑️ Dropped (kept for memory)
>
> Priority: **P1** = do soon · **P2** = normal · **P3** = someday/maybe
> Owner: `local` (desktop agent) · `cloud` (OCI server agent) — see COORDINATION.md
> Next ID counter: **T-008**

---

## 🔥 Active
<!-- Max 1–3 tasks. What's being worked on right now. -->

- [ ] **T-001** [P1] [owner: local] Verify model IDs `gemini-3.8-flash` / `qwen/qwen3.8-27b` against real Gemini/Groq model lists — likely invalid → 404 → 300s cooldown → gateway "looks dead"

## 📥 Backlog

- [ ] **T-003** [P2] Delete `diagnostics.py` (legacy startup API calls, superseded by gateway)
- [ ] **T-004** [P2] Clean backup/temp clutter (`api_clients.py.backup.*`, `assistant.py.backup.*`, `config.py.backup.*`, `temp/*.bak`) — now also on remote; plain commit removal is fine
- [ ] **T-005** [P2] Write a real README (what it is, setup, usage)
- [ ] **T-006** [P1] Add guardrails to `execute_bash` (currently `shell=True`, no allowlist) — required before OCI deploy
- [ ] **T-007** [P2] [owner: cloud] Cloud (OCI Mumbai) section of ACCESS.md — assigned to cloud-side agent

## ✅ Done

- [x] **T-002** Restore `.env` from `Infra\KEys.txt` (GEMINI + GROQ keys, gitignored, values never exposed) — 2026-10-04
- [x] **T-000** Push 9 pending commits to `origin/master` — 2026-10-04

## 🗑️ Dropped
<!-- Rejected / won't-fix, kept for memory. -->

- [ ] ~~Claude Code Proxy (paid API)~~ — abandoned ~2026-10-03, too expensive; replaced by direct Gemini+Groq cascade

---

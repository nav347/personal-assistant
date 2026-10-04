
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
> Next ID counter: **T-015**

---

## 🔥 Active
<!-- Max 1–3 tasks. What's being worked on right now. -->

- [ ] **T-001** [P1] [owner: local] Verify model IDs `gemini-3.8-flash` / `qwen/qwen3.8-27b` against real provider lists — likely invalid → 404 → 300s cooldown → gateway "looks dead"
  - [ ] 1. List real Gemini models — `GET https://generativelanguage.googleapis.com/v1beta/models` (key loaded from `.env`, read-only, never printed)
  - [ ] 2. List real Groq models — `GET https://api.groq.com/openai/v1/models` (Bearer key from `.env`, read-only, never printed)
  - [ ] 3. Compare lists vs config → correct the model IDs → commit fix
  - [ ] 4. Log findings in COORDINATION.md so the cloud agent sees them

## 📥 Backlog

- [ ] **T-013** [P1] **Environment-aware, self-evolving scripts** — replace ad-hoc manual commands with scripts that detect their environment and adapt
  - **Problem:** too much manual command-calling / one-off command creation each time; wasteful, inconsistent, not unified
  - **Goal:** a set of scripts that **sense the environment** (OS, paths, cloud vs local, tools present) and do the right thing automatically
  - **Self-evolving:** when a script hits an unexpected condition/issue, it should **adapt or record how to adapt** (e.g. fall back, patch itself, or log a fix) rather than requiring a human to hand-craft a new command next time
  - **Benefits:** cheaper (fewer bespoke LLM calls), more unified (one way to do each thing), reproducible
  - ⚠️ Open Qs: where do scripts live (repo `scripts/`)? how do they self-evolve safely (auto-edit vs propose-then-apply)? guardrails so "self-evolving" can't do damage?
- [ ] **T-010** [P1] **Unified harness — one unit, cloud + local, git-based setup**
  - Single codebase that runs **identically** on the OCI cloud server and the local desktop (same entrypoint, same config surface)
  - **Setup = clone + configure** — no bespoke per-machine steps; everything reproducible through git
  - Environment differences (paths, credentials, host) handled by config/env, not code forks
  - ⚠️ Open Qs: single repo vs submodule for the harness? how does it relate to the existing personal-assistant code?
- [ ] **T-011** [P1] **SOPS encryption so keys can live in git**
  - Encrypt `.env` (and any secret files) with [SOPS](https://github.com/getsops/sops) → commit ciphertext to the repo safely
  - Key management: age key (recommended) or cloud KMS; document the decrypt workflow
  - Enables the cloud agent to pull secrets via git without manual copying
  - ⚠️ Depends on / pairs with T-010 (git-based setup)
- [ ] **T-012** [P2] **Harness editor UI — Claude-like input box, extensible**
  - Interactive editor/REPL with a proper input box (multi-line, history, cursor editing) similar to the Claude CLI
  - Built to be **extended** — user will add features as needed (e.g. `/btw`, `/past` from T-009)
  - ⚠️ Open Qs: TUI framework (Textual/rich vs plain readline)? terminal-only or also web?
- [ ] **T-009** [P2] Custom harness: add `/btw` and `/past` commands
  - **`/btw`** — quick aside capture: dump a thought/note mid-conversation without derailing the current task; persisted durably (file, not just chat history) so it survives context compaction
  - **`/past`** — recall past context: surface previous session summaries / search past notes on demand
  - ⚠️ Open questions: exact storage location for `/btw` notes (new `NOTES.md` vs append to TASKS.md?), and whether `/past` filters by keyword/date. Clarify with user before building
- [ ] **T-014** [P1] Editor must never get stuck — diagnose planner hangs FIRST
  - **Symptom:** planner sometimes gets stuck for long periods; **last full session got stuck too** (reported 2026-10-04)
  - **Rule:** diagnose root cause BEFORE building the T-012 editor, so the new editor inherits fixes, not the same bug
  - **Diagnostics wanted:** live loaders/spinners, last-call info, elapsed time, retry state — visible instead of silent freeze
  - ⚠️ Open Qs: hang = provider timeout? tool call never returning? REPL loop waiting on stdin? (need logs from a stuck run — collect on next occurrence; if agent is stuck, how does the user escape/save state first?)
- [ ] **T-008** [P2] Context/memory strategy for long sessions — **phased, classifier LAST**:
  1. **File-state first (done):** durable facts live in repo files (TASKS.md, COORDINATION.md, ACCESS.md) → chat history is disposable
  2. **Token-trigger compaction:** when history > N tokens, one cheap LLM call summarizes turns older than last K; keep a **pinned-facts block** (identity, key locations, current task, decisions) that is never compressed. No classifier — trigger is a token count
  3. **Importance scorer (only if summaries lose facts):** cheap LLM call rating each turn 0–10, or embeddings + retrieval (pull relevant old context on demand) — NOT a trained ML classifier (no training data, silent misclassification = data loss)
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

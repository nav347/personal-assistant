# Project State Tracker

Persistent memory for assistant sessions. Read this FIRST at session start,
update it after meaningful work, commit the update. Keep it small — do not
re-read the whole codebase every session (rate-limit friendly).

Companion doc: **ACCESS.md** — single source of truth for how the assistant
is accessed/run (local vs cloud). Update both when access changes.

_Last updated: 2026-10-03 (session 2 with CLI assistant)_

## Goal

Get the **Personal OS agent** up and running.

- Development happens **locally (Windows laptop)** first — faster iteration.
- Deployment target: **Oracle Cloud (OCI)** — already set up, do not re-do.
- Move to OCI only once local development is stable.
- **The git repo is the single source of truth** for project state, decisions,
  and access methods (see ACCESS.md).

## Infra & assets

| Asset | Location |
|---|---|
| OCI instance | Oracle **Mumbai**, 1GB (free tier) |
| OCI SSH keys | `OneDrive\Desktop\NAV347\Infra\Mumbai 1gb instance\ssh-key-oracle-mumbai-1gb.key` |
| GCP service account | `OneDrive\Desktop\NAV347\Infra\GCP-service-account-navpersonalasst-7e854324d6f3.json` |
| API keys backup | `OneDrive\Desktop\NAV347\Infra\KEys.txt` (DO NOT print contents) |
| Repo remote | `github.com/nav347/personal-assistant` |

## Current codebase state

Working CLI agent in repo root:

- `assistant.py` — REPL (`/paste` multiline, `/status`), JSON-command agent loop
- `api_clients.py` — unified gateway: gemini → groq cascade, per-model cooldowns
  (429→60s, 5xx→20s, timeout→30s, config→300s), no API calls at startup
- `config.py` — loads `.env` (GEMINI_API_KEY, GROQ_API_KEY) + `personal_os.md` as system prompt
- `tools.py` — `execute_bash()` (shell=True, 30s timeout, no guardrails yet)
- `personal_os.md` — the Personal OS philosophy / system prompt (read-only reference)
- `ACCESS.md` — how to access/run the assistant (local verified; cloud TBD)

## Blockers / next steps

1. **`.env` is MISSING locally** — restore GEMINI_API_KEY / GROQ_API_KEY from
   `Infra\KEys.txt`, then the agent runs locally.
2. **Verify model IDs** — `gemini-3.8-flash` and `qwen/qwen3.8-27b` look
   suspicious; if invalid, every call 404s → 300s cooldown → gateway looks dead.
   Check against real provider model lists.
3. **Document cloud access in ACCESS.md** — user says cloud access differs
   from local; details not yet written down (SSH command, repo location on
   server, how it runs there).
4. `diagnostics.py` is legacy (makes startup API calls, contradicts current
   design) — delete or rewrite.
5. Clean up `*.backup.*` files and `temp/*.bak` once stable.
6. Before OCI deployment: add a confirmation/allowlist policy to `execute_bash`.

## History / decisions

- **2026-10-03** — initial harness built, then refactored into the unified
  gateway design (backups in `temp/` + `*.backup.*`).
- **2026-10-03 (session 2)** — added `PROJECT_STATE.md` + `ACCESS.md` as
  repo-internal source of truth. Branch audit: `main` = real project,
  `master` = empty GitHub-init stub (cleanup optional, not urgent).
- **Claude Code Proxy — ABANDONED.** ~1 day spent on
  `%USERPROFILE%\claude-code-proxy` (Anthropic-compatible proxy, 15 provider
  backends) trying to run a Claude harness. Too expensive; settled on **direct
  simple API calls (Gemini + Groq) with no Claude harness**. Do not revisit
  unless the user asks. (`%USERPROFILE%\anthropic-proxy` — earlier node
  experiment, also not part of this project.)

## Session protocol (for the assistant)

- Start: read this file + `ACCESS.md` + `git log --oneline -5`. Enough context.
- After meaningful work: update this file (+ ACCESS.md if access changed),
  then commit (`docs: update project state`).
- Never print or commit secrets. `.env` is gitignored — keep it that way.
- Ask before destructive actions (per `personal_os.md`).
- The git repo is the source of truth — if knowledge isn't in the repo,
  get it into the repo.

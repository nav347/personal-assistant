# 🤝 Agent Coordination

> **This repo is the coordination bus.** No SSH, no direct server access — all
> communication between agents happens exclusively through commits to `master`.

## 👥 Agents

| ID | Agent | Environment | Scope |
|----|-------|-------------|-------|
| `local` | Local desktop agent (Claude Code CLI) | Windows 11 desktop, this repo | Local tasks, code, docs |
| `cloud` | Cloud-side agent | OCI Mumbai server | Cloud tasks (T-007: ACCESS.md cloud section) |

## 🔐 Environment Notes

- **Git auth (local):** GitHub credentials are stored in **Windows Credential Manager**
  (`git:https://github.com`) via Git Credential Manager. Pushes/pulls are **silent —
  no login prompt**. If a push ever hangs or pops an auth window, the cached token
  went stale: complete the one-time re-auth (or kill the hung `git-credential-manager`
  process and retry), and the new token is cached again automatically.
- **Secrets:** `.env` is gitignored and holds GEMINI/GROQ keys (restored from
  `Infra\KEys.txt`). Never print, commit, or transmit key values — copy file→file only.

## 📐 Protocol — every agent, every session

1. **PULL first** — `git pull origin master` before doing anything. The remote may have moved.
2. **CLAIM before work** — move the task to 🔥 Active in `TASKS.md`, tag owner + date
   (e.g. `**T-003** [P2] ... — claimed by local 2026-10-04`), commit, push.
   If the push conflicts → someone else claimed it: re-pull and pick another task.
3. **WORK** — small focused commits referencing task IDs: `T-003: remove diagnostics.py`.
4. **REPORT after** — move the task to ✅ Done (or back to 📥 Backlog with a note why),
   append a line to the 📡 Log below, commit, push.
5. **MESSAGES** — need the other agent to know/decide something? Append to the 📡 Log.
   They will read it on their next pull. Never assume the other agent saw anything
   until it's in a pushed commit.

## 📡 Log
<!-- Append-only. Newest at TOP. Format: `- YYYY-MM-DD HH:MM [agent] message` -->

- 2026-10-04 15:58 [local] Documented git auth setup in Environment Notes: GCM token cached in Windows Credential Manager → pushes are silent, no login needed. One-time re-auth only if token goes stale.
- 2026-10-04 15:54 [local] Coordination protocol established (COORDINATION.md + TASKS.md owner tags). Next up for local: T-001 (verify model IDs). Cloud agent: T-007 remains yours — pull before working.
- 2026-10-04 15:54 [local] T-002 done earlier today: `.env` restored from Infra\KEys.txt (file→file copy, values never exposed, gitignored). Repo fully pushed through `2bd01c6`.

# Access — Single Source of Truth

How this Personal OS assistant is accessed and run.
This file is the authoritative record. Update it whenever access changes.
If it isn't written here, it doesn't exist.

> **Security rule:** this repo is PUBLIC. Never commit IPs, usernames,
> keys, or credentials. Private connection details live in
> `ACCESS.local.md` (gitignored, local only).

## Local (Windows laptop) — current dev environment

Repo: `OneDrive\Desktop\NAV347\Personal\personal-assistant\personal-assistant`
(branch: `main`)

### How to run

```text
cd OneDrive\Desktop\NAV347\Personal\personal-assistant\personal-assistant
python assistant.py
```

### Requirements

- Python 3.9+ (pyc cache shows cpython-39)
- `.env` in repo root containing:
  - `GEMINI_API_KEY=...`
  - `GROQ_API_KEY=...`
- `pip install requests`

### In-session commands

| Command | Effect |
|---|---|
| `exit` / `quit` | close session |
| `/paste` … `/end` | multiline input mode (`/cancel` discards) |
| `/status` | show provider/model cooldown state (no API calls) |

### How the agent works

Model replies with JSON `{"thought": "...", "command": "..."}` → command is
executed in the local shell → terminal output fed back for a summary turn.
Plain-text replies are just printed.

### Current local status (2026-10-03)

- ❌ `.env` missing → agent cannot start until keys are restored
  (keys backup: `NAV347\Infra\KEys.txt` — do not commit or print)

## Cloud (Oracle OCI Mumbai) — deployment target

Instance: Oracle Mumbai, 1GB free tier. SSH key:
`NAV347\Infra\Mumbai 1gb instance\ssh-key-oracle-mumbai-1gb.key`

**SSH connection command:** see `ACCESS.local.md` (gitignored — kept out of
this public repo intentionally).

> **Status: TO BE FILLED BY THE CLOUD-SIDE AGENT** (per user, 2026-10-03).
> The agent running on the OCI instance is responsible for documenting its
> own environment in this section:
>
> - [ ] Where the repo lives on the server
> - [ ] How the assistant runs there (tmux/screen/systemd/bare?)
> - [ ] How `.env` is provided on the server
> - [ ] How the user reaches the assistant from outside (SSH? web? other?)
> - [ ] Anything tried that failed

## What was tried before (access history)

| Attempt | Outcome |
|---|---|
| Claude Code Proxy (`%USERPROFILE%\claude-code-proxy`, ~1 day) | ❌ Abandoned — Claude harness too expensive |
| Direct simple API (Gemini + Groq, no harness) | ✅ Current approach |
| `anthropic-proxy` (node, home dir) | Earlier experiment, not part of this project |

## Repo layout notes

- `main` branch = the real project.
- `master` branch = empty GitHub-init stub (2-line README). Harmless; can be
  cleaned up later by making `main` the default on GitHub and deleting `master`.

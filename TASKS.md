



# ≡ƒôï Task Backlog

> **Workflow:**
> - **Add:** say `add task: <description>` ΓÇö I append it with the next ID
> - **Pick:** say `pick a task` ΓÇö I suggest the highest-priority unclaimed one
> - **Claim:** move to ≡ƒöÑ Active with owner + date, commit, push (see COORDINATION.md)
> - **Done:** say `done: T-XXX` ΓÇö I move it to Γ£à Done with the date
> - **Drop:** say `drop: T-XXX` ΓÇö moved to ≡ƒùæ∩╕Å Dropped (kept for memory)
>
> Priority: **P1** = do soon ┬╖ **P2** = normal ┬╖ **P3** = someday/maybe
> Owner: `local` (desktop agent) ┬╖ `cloud` (OCI server agent) ΓÇö see COORDINATION.md
> Next ID counter: **T-048**

---

## ≡ƒöÑ Active
<!-- Max 1ΓÇô3 tasks. What's being worked on right now. -->

- [ ] **T-001** [P1] [owner: local] Verify model IDs `gemini-3.8-flash` / `qwen/qwen3.8-27b` against real provider lists ΓÇö likely invalid ΓåÆ 404 ΓåÆ 300s cooldown ΓåÆ gateway "looks dead"
  - [ ] 1. List real Gemini models ΓÇö `GET https://generativelanguage.googleapis.com/v1beta/models` (key loaded from `.env`, read-only, never printed)
  - [ ] 2. List real Groq models ΓÇö `GET https://api.groq.com/openai/v1/models` (Bearer key from `.env`, read-only, never printed)
  - [ ] 3. Compare lists vs config ΓåÆ correct the model IDs ΓåÆ commit fix
  - [ ] 4. Log findings in COORDINATION.md so the cloud agent sees them

## ≡ƒôÑ Backlog

- [ ] **T-047** [P1] Keys must always be available: git first, else server + local copy
  - Private/public keys available in git if possible (ties to T-011 SOPS encryption)
  - Otherwise: key lives on server AND a copy exists locally (redundancy)
  - Never leave a key in exactly one place ΓÇö always have a recoverable copy
  - Document where each key lives (git / server / local) in ACCESS.md
  - Keys stay out of plaintext commits; encrypted-in-git or outside-git only
- [ ] **T-046** [P2] Re-evaluate the importance of keepalive property
  - Assess current requirements and constraints of the project
  - Determine whether keepalive is still a priority right now
  - Consider alternatives if keepalive isn't feasible / needed yet
  - Update plan/task list accordingly and document the decision
- [ ] **T-045** [P1] Monitor current state of infra and resources
  - System to track + display current infra and resource usage
  - Real-time updates and alerts for changes/issues
  - Integrate with existing monitoring and health-check tools
  - Use the data to inform decisions and optimize allocation
  - Continuously evaluate and improve the system
- [ ] **T-044** [P2] Consider giving the assistant a personality (optional)
  - Explore traits that would be useful/engaging (tone, humor, preferences)
  - Prototype personality features if desired
  - Ensure personality never interferes with correctness or clarity
  - Decide later ΓÇö only if it genuinely improves the experience
- [ ] **T-043** [P3] Build the ultimate context for our work
  - Develop comprehensive understanding of the context our work is used in
  - Capture context in a machine-readable format
  - Keep it accurate, up-to-date, and relevant per task
  - Use context to inform and improve model accuracy and workflows
  - Continuously refine for accuracy and token-efficiency
- [ ] **T-042** [P2] Automate raising fixes or PRs based on context
  - Auto-raise fixes/PRs from detected mistakes (links to T-041)
  - Context-aware: respects each project's requirements
  - Integrate with existing workflow; add a review gate
  - Measure accuracy of auto-raised fixes/PRs
- [ ] **T-041** [P1] Implement mistake detection and auto-fixing in transcripts
  - Detect mistakes in dictation/transcripts (typos, formatting)
  - Auto-fix detected mistakes; context-aware + token-efficient
  - Integrate with existing workflow
  - Continuously evaluate detection/fix accuracy
- [ ] **T-040** [P3] Add more models and explore alternative LLMs
  - Research/evaluate alternative LLMs + their free tiers
  - Add new models to the system to increase capability
  - Investigate combining multiple models for better results
  - Monitor and refresh the model portfolio over time
- [ ] **T-039** [P2] Sign up for multiple accounts to leverage free tiers
  - Multiple accounts to multiply free-tier limits
  - Track/manage accounts cleanly; config, not sprawl
  - Monitor usage to avoid hitting limits
  - Respect ToS ΓÇö explore what's legitimately allowed
- [ ] **T-038** [P1] Explore fallback chunking & parallel processing with multiple accounts
  - Fallback chunking to maximize free-tier usage
  - Parallel processing across multiple accounts
  - Research + test techniques; refine by measurement
  - Comply with free-tier limits and ToS
- [ ] **T-037** [P2] Aim for 80%+ protocol coverage within 2 years
  - Target protocols for ~80% of recurring tasks in 2 years
  - Prioritize by frequency, complexity, impact
  - Review coverage periodically; celebrate milestones
- [ ] **T-036** [P1] Establish protocols & step-by-step guides for all tasks
  - Standardized, documented protocols/checklists for tasks
  - Review + refine to keep effective
  - Follow protocols ΓÇö but not blindly; critical thinking always
- [ ] **T-035** [P2] Environment reorganization & diagnostics when needed
  - Auto-detect/organize env on startup (per T-013 self-evolving)
  - Diagnose on demand when something breaks
  - Reuse T-014 diagnostics to surface hangs/failures
- [ ] **T-034** [P1] Regular monitoring, health checks & startup diagnostics
  - Periodic health checks: what's working / what's not
  - Startup diagnostics (env organization, config, connectivity)
  - Clear dashboard/log of component status
  - Alert before failures cascade (keepalive, Oracle, API)
  - Runs automatically + on-demand (`/status`)
- [ ] **T-033** [P3] Develop a visually appealing and interactive interface for free models
  - Intuitive, user-friendly UI for free models
  - Interactive elements; engaging visuals/animations
  - Responsive across devices; validate with user feedback
- [ ] **T-032** [P2] Improve routing for free models, visuals, and inner workings
  - Streamline routing for free models (less friction)
  - Enhance visuals ΓÇö engaging, intuitive, expandable for power users
  - Refine inner workings for performance/efficiency
  - Test to validate improvements
- [ ] **T-031** [P2] Plan for potential database integration in the future
  - Shortlist DB options (MySQL, PostgreSQL, MongoDBΓÇª)
  - Consider data structure, scalability, integration ease
  - Migration plan if a DB is needed later
  - Flexible plan that adapts to changing requirements
- [ ] **T-030** [P1] Evaluate database needs vs MD files & Excel tracking
  - Decide: DB needed now, or MD/Excel enough to start?
  - Weigh scalability vs simplicity
  - Get started soon ΓÇö don't block on a DB decision
- [ ] **T-029** [P2] Append "Never pay" principle to assistant OS core rules
  - Record T-028 as a top-level standing rule
  - Standing check: any new tool/service must be free-tier
  - Surfaces before any cost decision (Oracle, APIs, storage)
- [ ] **T-028** [P1] PRINCIPLE: Never pay ΓÇö stay free as long as possible
  - Core stance: free tier only; avoid all paid services
  - Pay only if truly necessary after exhausting free options
  - Re-verify free-tier limits before any payment
  - Revisit only when a real need forces it
- [ ] **T-027** [P1] Script to keep Oracle servers alive (prevent shutdown)
  - Keepalive script so instances don't get shut down
  - Runs periodically to detect/prevent idle-shutdown
  - Lives in repo `scripts/` (fits T-013 self-evolving)
  - Applies to current 1GB AMD + future 8GB ARM
- [ ] **T-026** [P2] Obtain 8GB ARM instance on Oracle (scale-up later if needed)
  - 6GB/24GB ARM not obtainable ΓåÆ adjusted to 1GB AMD for now
  - Target: acquire an 8GB ARM instance (highest obtainable now)
  - Plan to scale up later if needs grow
  - Keep 1GB AMD as fallback until 8GB is live
- [ ] **T-025** [P2] Set reminder to check Oracle account in 28 days
  - Schedule reminder to review Oracle account activity
  - Verify no additional unexpected charges occurred
  - Confirm initial charge was error/resolved (ties to T-024)
- [ ] **T-024** [P1] Investigate $2.76 charge on Oracle account
  - Check Oracle account for unexpected charges
  - Verify if related to services/subscriptions
  - Determine if error or legitimate fee
  - Follow up in 28 days to confirm resolved
- [ ] **T-013** [P1] **Environment-aware, self-evolving scripts** ΓÇö replace ad-hoc manual commands with scripts that detect their environment and adapt
  - **Problem:** too much manual command-calling / one-off command creation each time; wasteful, inconsistent, not unified
  - **Goal:** a set of scripts that **sense the environment** (OS, paths, cloud vs local, tools present) and do the right thing automatically
  - **Self-evolving:** when a script hits an unexpected condition/issue, it should **adapt or record how to adapt** (e.g. fall back, patch itself, or log a fix) rather than requiring a human to hand-craft a new command next time
  - **Benefits:** cheaper (fewer bespoke LLM calls), more unified (one way to do each thing), reproducible
  - ΓÜá∩╕Å Open Qs: where do scripts live (repo `scripts/`)? how do they self-evolve safely (auto-edit vs propose-then-apply)? guardrails so "self-evolving" can't do damage?
- [ ] **T-010** [P1] **Unified harness ΓÇö one unit, cloud + local, git-based setup**
  - Single codebase that runs **identically** on the OCI cloud server and the local desktop (same entrypoint, same config surface)
  - **Setup = clone + configure** ΓÇö no bespoke per-machine steps; everything reproducible through git
  - Environment differences (paths, credentials, host) handled by config/env, not code forks
  - ΓÜá∩╕Å Open Qs: single repo vs submodule for the harness? how does it relate to the existing personal-assistant code?
- [ ] **T-011** [P1] **SOPS encryption so keys can live in git**
  - Encrypt `.env` (and any secret files) with [SOPS](https://github.com/getsops/sops) ΓåÆ commit ciphertext to the repo safely
  - Key management: age key (recommended) or cloud KMS; document the decrypt workflow
  - Enables the cloud agent to pull secrets via git without manual copying
  - ΓÜá∩╕Å Depends on / pairs with T-010 (git-based setup)
- [ ] **T-012** [P2] **Harness editor UI ΓÇö Claude-like input box, extensible**
  - Interactive editor/REPL with a proper input box (multi-line, history, cursor editing) similar to the Claude CLI
  - Built to be **extended** ΓÇö user will add features as needed (e.g. `/btw`, `/past` from T-009)
  - ΓÜá∩╕Å Open Qs: TUI framework (Textual/rich vs plain readline)? terminal-only or also web?
- [ ] **T-009** [P2] Custom harness: add `/btw` and `/past` commands
  - **`/btw`** ΓÇö quick aside capture: dump a thought/note mid-conversation without derailing the current task; persisted durably (file, not just chat history) so it survives context compaction
  - **`/past`** ΓÇö recall past context: surface previous session summaries / search past notes on demand
  - ΓÜá∩╕Å Open questions: exact storage location for `/btw` notes (new `NOTES.md` vs append to TASKS.md?), and whether `/past` filters by keyword/date. Clarify with user before building
- [ ] **T-014** [P1] Editor must never get stuck ΓÇö diagnose planner hangs FIRST
  - **Symptom:** planner sometimes gets stuck for long periods; **last full session got stuck too** (reported 2026-10-04)
  - **Rule:** diagnose root cause BEFORE building the T-012 editor, so the new editor inherits fixes, not the same bug
  - **Diagnostics wanted:** live loaders/spinners, last-call info, elapsed time, retry state ΓÇö visible instead of silent freeze
  - ΓÜá∩╕Å Open Qs: hang = provider timeout? tool call never returning? REPL loop waiting on stdin? (need logs from a stuck run ΓÇö collect on next occurrence; if agent is stuck, how does the user escape/save state first?)
- [ ] **T-008** [P2] Context/memory strategy for long sessions ΓÇö **phased, classifier LAST**:
  1. **File-state first (done):** durable facts live in repo files (TASKS.md, COORDINATION.md, ACCESS.md) ΓåÆ chat history is disposable
  2. **Token-trigger compaction:** when history > N tokens, one cheap LLM call summarizes turns older than last K; keep a **pinned-facts block** (identity, key locations, current task, decisions) that is never compressed. No classifier ΓÇö trigger is a token count
  3. **Importance scorer (only if summaries lose facts):** cheap LLM call rating each turn 0ΓÇô10, or embeddings + retrieval (pull relevant old context on demand) ΓÇö NOT a trained ML classifier (no training data, silent misclassification = data loss)
- [ ] **T-003** [P2] Delete `diagnostics.py` (legacy startup API calls, superseded by gateway)
- [ ] **T-004** [P2] Clean backup/temp clutter (`api_clients.py.backup.*`, `assistant.py.backup.*`, `config.py.backup.*`, `temp/*.bak`) ΓÇö now also on remote; plain commit removal is fine
- [ ] **T-005** [P2] Write a real README (what it is, setup, usage)
- [ ] **T-006** [P1] Add guardrails to `execute_bash` (currently `shell=True`, no allowlist) ΓÇö required before OCI deploy
- [ ] **T-007** [P2] [owner: cloud] Cloud (OCI Mumbai) section of ACCESS.md ΓÇö assigned to cloud-side agent

## Γ£à Done

- [x] **T-002** Restore `.env` from `Infra\KEys.txt` (GEMINI + GROQ keys, gitignored, values never exposed) ΓÇö 2026-10-04
- [x] **T-000** Push 9 pending commits to `origin/master` ΓÇö 2026-10-04

## ≡ƒùæ∩╕Å Dropped
<!-- Rejected / won't-fix, kept for memory. -->

- [ ] ~~Claude Code Proxy (paid API)~~ ΓÇö abandoned ~2026-10-03, too expensive; replaced by direct Gemini+Groq cascade

---

<!-- NEW-SESSION-2026-10-04: T-024..T-044 dictated by user, re-captured after earlier writes failed to persist.
     2026-10-04 (2nd pass): T-045 (infra/resource monitoring), T-046 (re-evaluate keepalive), T-047 (keys available gitΓåÆserver+local) ΓÇö re-captured AGAIN after confirmations were wrong; verified against git log 6209088. -->

T-048 [P1] Life Tracker: track apps to build
   ├─ Create a section in Life Tracker for apps to build
   ├─ Add initial app ideas
   ├─ Use Life Tracker to monitor progress and reflect on experiences
   ├─ Continuously update and refine the list of apps to build
   └─ Explore ways to integrate Life Tracker with other tools and systems

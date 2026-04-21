# Session Checkpoint — HD-Dev Bootstrap + Architectural Insights

> **Purpose:** this document exists because the session that produced it was approaching compaction. Its job is to let any subsequent Claude instance rehydrate enough context to continue the work without starting over. Read this first on cold start if any of the following terms are live in the current conversation: "HD-Dev," "Will Kreth," "HAND," "wiki-compile," "Karpathy pattern," "Project Bootstrap Playbook," or "Skyline Boulevard."
>
> **Last updated:** 2026-04-21, near the end of a multi-day session that ran passes 1–6 of the HD-Dev bootstrap.

---

## What happened in this session (1-paragraph summary)

Joey consulted with Will Kreth (founder of Human & Digital, Inc. / HAND) on bootstrapping a Claude-native knowledge base for his startup. Over ~3 days we ran 6 compilation passes on Will's source documents, producing a 30+ file wiki at `/Users/joeyanuff-m2/Development/HD-Dev/wiki/`. The work was formalized as a reusable `/wiki-compile` skill and documented as Project Bootstrap Playbook v0.2 (in `drafts/`). Several architectural patterns emerged through the back-and-forth — they're the most important artifact of the session, captured below.

---

## Current state

### HD-Dev (Will's repo, github.com/humandigital-tech/HD-Dev)

- **PR #1** (`bootstrap-wiki-compilation` branch, fork at `januff:HD-Dev`) — **merged per Will's 2026-04-20 text: "Your PR is now merged in Git."**
- **Last push:** commit `c2c436d` — Pass 6 (structural cleanup + SOURCES.md + commit-by-default)
- **Passes completed:**
  1. **Pass 1** (2026-04-19) — 3 source files → CBN methodology article + scaffolding
  2. **Pass 2** (2026-04-19) — 6 additional files → 2 concepts + GLOSSARY + WHO; terminology collision surfaced
  3. **Pass 3** (2026-04-19) — no new sources → 5 new concept articles + DECISIONS
  4. **Pass 4** (2026-04-19) — no new sources → 6 person articles + 5 event articles + TIMELINE
  5. **Pass 5** (2026-04-20) — Resolution newsletter → Licensed Human Likeness article + 2 event articles + amendments + soft patent flag
  6. **Pass 6** (2026-04-20) — structural cleanup → consolidated documents/, added SOURCES.md inventory, commit-by-default convention
- **Wiki state:** 9 concept articles, 6 person articles, 7 event articles, 5 spine files (GLOSSARY, WHO, TIMELINE, DECISIONS, SOURCES), 1 summary doc
- **Raw documents:** 10 files totaling ~5 MB in `raw/documents/`
- **Unprocessed raw docs (gap surfaced in SOURCES.md):**
  - `Human & Digital — humandigital.tech.html` — 0 citations
  - `Will Kreth _ LinkedIn.html` — 0 citations
- **Pending team decisions (DECISIONS.md):** 8 items, grouped by decider (Will, John, Josh, etc.)
- **Patent-disclosure flag:** one soft flag from Pass 5 — LHL "authoritative record" phrasing adjacent to Claim 2 territory; counsel review recommended

### claude-code-tips (our repo)

- **Last commit:** `02e3a58` — `/wiki-compile` skill update (SOURCES.md dedup + inventory maintenance)
- **Key artifacts:**
  - `drafts/PROJECT_BOOTSTRAP_PLAYBOOK.md` — v0.2 (needs v0.3 revision with session learnings)
  - `drafts/hd-will-export-instructions.md` — sent to Will, never acted on (superseded by paste-this-doc pattern)
  - `.claude/commands/wiki-compile.md` — the skill (auto-registers in Claude Code sessions; shows up in the skill listing)
  - `analysis/2026-04-19-hd-dev-bootstrap-trial.md` — running notes through Pass 5
  - `analysis/2026-04-21-session-checkpoint.md` — this file
- **Our wiki (separate, older):** `Claude Code Tips/` Obsidian vault with 562 curated tips. This is a DIFFERENT project — do not conflate with HD-Dev.

---

## Architectural patterns discovered this session

These emerged through conversation. They are the session's most portable output. Each should land in the playbook v0.3.

### 1. Raw vs. wiki separation (Karpathy, promoted to load-bearing)
- `raw/` = unprocessed source material, committed by default
- `wiki/` = LLM-compiled synthesis layer
- Never edit raw files in place; new versions go alongside old ones
- Playbook v0.1 had this as an appendix; v0.2 promoted it to Core Principle 1

### 2. LLM writes the wiki; humans correct it
- Humans decide what *concepts* the wiki covers
- LLM drafts articles from raw sources
- Humans review and correct, don't draft from scratch
- This is the key shift for non-technical teammates — they can critique an LLM draft without being able to write one themselves

### 3. Obsidian optional, GitHub primary
- Original playbook led with "install Obsidian"
- Session discovered that for non-technical users, GitHub web viewer handles everything the wiki needs
- Obsidian is an upgrade path for power users, not a prerequisite
- All links use regular Markdown format (`[text](./path.md)`) not Obsidian wiki-links, so they work in GitHub + TextMate + Obsidian identically

### 4. Commit-by-default privacy convention (Pass 6 reframe)
- Original convention (v0.1): documents/ untracked, user decides what to commit
- Problem: creates confusion, breaks GitHub citation rendering, makes dedup impossible
- New convention (v0.2+): everything in `raw/documents/` is committed; exceptions get listed in `raw/PRIVATE.md` + `.gitignore`
- Repo privacy is handled at the repo level (private repo + collaborator access), not per-file

### 5. SOURCES.md as inverse-inventory spine file
- Wiki articles have Sources sections (each article lists what cites it)
- SOURCES.md is the inverse view: per-document, which articles cite it
- Includes SHA-256 hash (first 12 chars) for dedup on refeed
- Surfaces unprocessed raw material as a visible gap (0-citation rows)

### 6. DECISIONS.md + ASKS.md as human-loop ledger (ASKS.md not yet built)
- DECISIONS.md = things awaiting commitment from a named decider
- ASKS.md (proposed) = rolling queue of human-input-required items that don't yet have a decider assigned
- Together they're the complete human-in-the-loop surface — everything else can be Claude-to-Claude

### 7. Auto mode for non-technical users
- Claude Code has multiple permission modes: default (per-command approval), accept-edits, auto, bypass-permissions
- For a trusted user in a private repo doing predictable operations, auto mode is the right default
- Shift+Tab cycles modes; status bar shows current mode
- Saves one click per git/mv/edit operation, which compounds

### 8. Fork + PR flow for read-only outside contributors
- Original plan: push directly to the target repo
- Reality: Joey had read-only access to Will's repo, and forking was disabled
- Resolution: ask Will to toggle "Allow forking" in repo Settings (30-second admin action)
- Then: `gh repo fork` → push to fork → `gh pr create` from fork
- Works without requiring Will to grant write access
- This is the standard open-source contribution pattern; our playbook now documents it as the default for read-only contributors

### 9. Paste-the-whole-doc pattern (the real discovery)
- We spent significant effort designing a 6-step "what Will should do when the PR lands" walkthrough
- Will never opened the doc
- He collaborated anyway — by sending more raw material and trusting us to compile it
- **This is the real load-bearing loop:** raw material in → compilation happens → wiki grows → eventually human reviews
- Everything else is aspirational scaffolding
- Playbook v0.3: Step 5a (upload a document) should be the primary interaction mode, not one of several equal options

### 10. Claude-as-collaborator architecture (named late in session)
- Not just a tool preference — a team coordination model
- **Minimum team:** 2 humans × 2 Claudes each (terminal + app/web) × shared private git repo × 3 structured markdown files (STATUS.json, DECISIONS.md, ASKS.md)
- Each Claude reads the same artifacts; commits are the async message queue
- Humans become reviewers/approvers; Claudes handle synthesis, extraction, and routine updates
- This is the pattern Joey and Will are converging on (even if Will hasn't fully set up his terminal yet)

### 11. Speech-to-text + terminal + Remote Control as universal interface
- Karpathy's vibe-coding paradigm is intimately coupled with dictation
- For users with limited energy/typing capacity (Will is on chemotherapy), speech-to-text isn't a nice-to-have
- Claude Code terminal session + `claude --remote-control` = session is persistent on laptop, reachable from desktop-app Code tab, claude.ai web, Claude mobile app
- Built-in Claude dictation (no MacWhisper needed for MVP) on any of those surfaces
- This is not yet set up for HD-Dev; it's a future workstream to introduce when Will is ready

### 12. "Questions asked of the human" as a primary metric
- Through 6 passes with Will, we asked him zero questions
- All wiki content was derived from documents he'd already created
- The goal is to NEVER ask a human for something a document could answer
- Only the residual — genuinely-unresolved-in-sources items — should escalate to DECISIONS.md and (later) ASKS.md

---

## Playbook v0.3 backlog (what to roll into the next revision)

When we next revise `drafts/PROJECT_BOOTSTRAP_PLAYBOOK.md`:

- **Add SOURCES.md** to the standard spine files (currently listed: GLOSSARY, WHO, DECISIONS; add SOURCES)
- **Add ASKS.md** as a proposed spine file (inverse of DECISIONS; human-asks queue)
- **Reframe the privacy default** from "per-file discretion" to "commit-by-default, gitignore-exception-with-audit"
- **Demote the summary-doc walkthrough** from central to optional; promote Step 5a (document upload) to primary
- **Add the fork+PR flow** for read-only contributors
- **Add the auto-mode recommendation** (over per-command approval and bypass-permissions)
- **Add the Claude-as-collaborator architecture section** — this is its own major subsection
- **Add speech-to-text workstream** as a future note (not yet primary)
- **Add the "questions-asked-of-humans = 0" metric**
- **Update the "install Obsidian" section** to be optional/upgrade, not prerequisite
- **Document the paste-the-whole-doc pattern** as the working interaction mode

---

## Forward threads (not yet executed)

### Immediate (next session or soon)
1. **Process the two unprocessed raw docs** in HD-Dev — `Will Kreth_LinkedIn.html` and `humandigital.tech.html` are 0-citation items in SOURCES.md. Either Pass 7 processes them, or they stay as the visible gap reminder.
2. **Scaffold `wiki/ASKS.md`** on HD-Dev as the inverse-of-DECISIONS spine file. Should happen on next pass regardless of what triggers it.
3. **Add terminal-session setup to our own claude-code-tips workflow.** We don't yet have a terminal session with Remote Control for this project; adding one enables check-ins from phone while idle.

### Medium (after more source material)
4. **Build `/wiki-questions` skill** — periodic synthesis pass that groups pending DECISIONS + open questions across articles + ASKS.md items, clustered by decider, outputs `_ASKS_THIS_WEEK.md`. Timing: when DECISIONS.md grows past ~15 items or chat-archive is ingested.
5. **Help Will set up terminal + Remote Control** — when he signals readiness, walk him through the one-time setup. Right now his Pass 6 comments show he's on the desktop-app Code-tab path; terminal is a future upgrade.
6. **Ingest Will's chat archive** — his Billy-advisor Claude session has suggested he do this; we've held off waiting for targeted-slice request rather than full export.

### The Skyline Boulevard parallel project (Joey + brother Ed)
7. **Spin up the clone** — new home move in May; Joey + Ed moving in at different times. Ed is Claude-fluent (unlike Will), so setup is fast.
8. **Starter corpus:** Joey has existing Claude conversations about the area (one separate thread on questions about the new neighborhood). Move planning touches: vet, gym, primary care physician transitions; decor; organizational docs.
9. **Good for:** second case study of the playbook with a different user profile (power-user teammate vs. non-technical founder). Observed bootstrap on a local project we fully control.
10. **Initial address:** 8210 Skyline Boulevard.

### Playbook-level (after 2-3 more case studies)
11. **v0.3 of the playbook** — consolidates everything above + Claude-as-collaborator architecture section.
12. **Scheduled/looped processes** — Joey raised the idea of 6-hour cadence check-ins on GitHub status. Could be a `/wiki-status-check` skill or a scheduled task. Needs design.

---

## Will-specific context (for the next instance to carry forward)

- **Health context:** Will is at the tail end of chemotherapy for colon cancer. Brain fog is a real symptom. He is actively dealing with medical appointments (OT, PT, oncology). Joey is consciously calibrating asks to be extremely low-friction because of this. Do not ever imply this is a character issue — it's a gravity-level bias that applies to almost everyone in similar situations.
- **Collaboration posture:** Joey established with Will that he doesn't need payment or equity — he needs Will to follow through on the minimum asks because Joey is literally blocked until he does. This framing (blockers, not requests) worked.
- **Will's Claude is engaged.** His most recent message (2026-04-20 night, via his Claude in another session) showed genuine engagement with the wiki. Quoted: "I feel forensically examined!" His Claude is drafting context-aware responses and has recommended Path A (install Claude Code) and Path B (do exports in browser) thoughtfully.
- **Will has merged PR #1** as of 2026-04-20 late night (per his text to Joey).
- **Will has not yet added any new documents** beyond the Resolution newsletter. The collaboration stack is not yet bootstrapped — we're one-way-sender at this point.
- **Goal:** increasing tight communication between our Claude and Will's Claude, minimizing Will-in-the-loop events. Commit messages, STATUS.json recent_changes, and (eventually) ASKS.md become the shared coordination surface.
- **Will's teammates:** John Carlucci (CTO), Josh Perkins (Dev Lead), Gabriel Berger (CCO), Wynne Kim (VP Policy), Renard T. Jenkins (HAND Chairman), Raymond Drewry (HAND Advisor). None are yet in the loop directly; everything flows through Will for now.

---

## How to resume after context compaction

If you're picking up this thread after context has been compacted or a fresh session has been started:

1. **Read this file first.**
2. **Read `STATUS.json`** in both HD-Dev and claude-code-tips for machine-readable state.
3. **Read `drafts/PROJECT_BOOTSTRAP_PLAYBOOK.md`** in claude-code-tips for the current playbook version.
4. **Check `git log`** in both repos for the most recent commits; specifically note whether any new passes have happened since `c2c436d` (HD-Dev) or `02e3a58` (claude-code-tips).
5. **If Will has sent new material** (check `raw/documents/` for any file not in `wiki/SOURCES.md`), run `/wiki-compile` on it.
6. **If Joey is active and asking what to do,** the default next step is either:
   - Process the two unprocessed HD-Dev docs as Pass 7 (easiest)
   - Scaffold `wiki/ASKS.md` (if that hasn't already happened)
   - Spin up the Skyline Boulevard parallel project (new work)
   - Begin v0.3 of the playbook (consolidation work)

---

## Meta-observations on the session itself

Worth capturing because they'll inform how future sessions shape their work:

- **The session ran long because the work was genuinely generative.** We weren't just executing a plan — we were discovering patterns through iteration. Each pass surfaced something we hadn't anticipated. That's why simple "play through the playbook" descriptions undersell what happened.
- **Will's "I feel forensically examined" was the moment the wiki justified itself.** Before that, it was a theory. After, it was a thing a human felt when looking at it. That signal — the user's emotional response to a specifically-designed artifact — is the real proof the playbook works.
- **The paste-the-whole-doc insight was worth more than any specific code we wrote.** It inverted the design center. Playbook v0.3 should lead with this.
- **Joey's parallel projects (Skyline, and implicitly others) are the test that the playbook generalizes.** If it works for a startup founder's knowledge base AND a house move AND whatever else, we know it's architecture, not one-off.

---

*This checkpoint exists because Joey explicitly asked for it near 76% context. Its existence is itself an instance of the pattern: substantiate-through-documents rather than substantiate-through-memory. When in doubt about what to write, write it down.*

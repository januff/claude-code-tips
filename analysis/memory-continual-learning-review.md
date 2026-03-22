# Memory & Continual Learning: Literature Review

> Generated: 2026-03-21
> Source: Our database of 562 Claude Code community tips
> Purpose: Understand what solutions exist before building our own

---

## Category 1: Official/First-Party Features

These are shipped by Anthropic. They represent the "default" answer to "why didn't you just use X?"

| Feature | Likes | Author | What it does | Our status |
|---------|------:|--------|-------------|------------|
| **/btw** | 24,025 | @trq212 | Side conversations while Claude works, preserving main context | Not yet adopted |
| **Dispatch** | 17,270 | @felixrieseberg | Persistent conversation across devices via Cowork | Not yet available to us (research preview) |
| **Auto-Memory** | 4,164 | @trq212 | Claude remembers across sessions — project context, patterns, styles | Using (MEMORY.md), but haven't evaluated the new auto-memory feature |
| **Launch from phone** | 4,628 | @bcherny | Start Claude Code on laptop from phone | Not explored |
| **--teleport** | 800 | @chongdashu | Sync desktop session with web/mobile | Not explored |
| **Compaction (v2.1.3)** | 1,164 | @nummanali | Auto-compaction works with Plan Mode + Todo list | Using compaction + pre-compact hook |
| **cleanupPeriodDays** | 905 | @repligate | Prevent auto-deletion of old sessions | ✅ Set to 99999 |
| **context: fork** | 588 | @lydiahallie | Run skills in isolated subagent | ✅ Using in skill frontmatter |

### What we should evaluate next:
- **Auto-Memory**: How does it compare to our manual MEMORY.md approach? Does it capture the right things? Use as a control group against our deeper approaches.
- **/btw**: Joey has used it a few times. Rarely needed because tasks finish before addenda arise. Low priority.
- **Dispatch**: Watch for general availability. Could solve the multi-device problem.

### Tested 2026-03-21:
- **/rc, /remote-control**: Returned "Unknown skill" in desktop app Code tab (v2.1.81, well past v2.1.51 requirement). These are built-in CLI commands, not "skills," and the desktop app's Code tab doesn't expose them. Documentation says `/remote-control` works "from an existing session" but this appears to mean terminal sessions only. **Gap:** desktop app Code tab users cannot enable Remote Control mid-session. Workaround: start a terminal session with `claude --remote-control` instead.
- **/teleport**: Also "Unknown skill" — may be deprecated or renamed to Remote Control. The @chongdashu tweet (800 likes) references `--teleport` but current docs use `--remote-control`.

---

## Category 2: Community Memory Solutions

Third-party tools and plugins. These are the "have you tried X?" answers.

| Solution | Likes | Author | What it does | Our status |
|----------|------:|--------|-------------|------------|
| **Smart Forking** | 4,632 | @PerceptualPeak | Uses past sessions to inform new features via /fork-detect | Not explored |
| **Claude-Mem** | 3,222 + 1,177 | @LiorOnAI, @simplifyinAI | Plugin for persistent memory across sessions | Not explored |
| **Continuous Claude v2** | 1,019 | @parcadei | System designed to manage context as scarcest resource | Not explored |
| **QMD + sync-claude-sessions** | 548 | @tomcrawshaw01 | Makes sessions searchable, auto-exports to markdown | Not explored — but our digest script does similar |
| **Theorist layer** | 385 | @blader | Continuously updated "theory of what's happening" for long sessions | Not explored — conceptually similar to our STATUS.json |

### What we should evaluate next:
- **Claude-Mem**: 4,400 combined likes. Is this better than our manual approach?
- **Smart Forking**: The /fork-detect concept is intriguing — could we use it?
- **Theorist layer**: Closest conceptually to what we're building. Read the full thread.
- **QMD**: Compare to our digest_sessions.py — are they solving the same problem?

---

## Category 3: Context Management Patterns

Techniques and workflows, not tools. These are the "how should you think about it?" answers.

| Pattern | Likes | Author | Key insight |
|---------|------:|--------|------------|
| **state.md** | 2,202 | @SearchForRyan | Explicit project scope speeds up changes from 8-10 mins to seconds |
| **CLAUDE.md half-life** | 423 | @toddsaunders | Rewrite CLAUDE.md from scratch every few weeks. It accumulates technical debt. |
| **Ralph Wiggum loop** | 3,607+ | Multiple | Keep-it-simple auto-restore pattern for long-running tasks |
| **Handoff skill** | 509 | @zeroxBigBoss | Self-contained prompts for context-less agent handoffs |
| **Clone repos into /tmp/** | 1,021 | @RhysSullivan | Agent learns from good repos by cloning them temporarily |
| **Workflow Orchestration** | 1,321 | @JackCulpan | Plan mode default, subagent utilization, continuous self-improvement |

### Our adoption status:
- **state.md**: We use STATUS.json (similar concept, machine-readable). ✅
- **CLAUDE.md half-life**: We haven't rewritten CLAUDE.md from scratch since Feb. May be due.
- **Ralph Wiggum**: Aware of it, haven't formally adopted. Our pre-compact hook is a simpler version.
- **Handoff skill**: We retired handoffs in favor of code-tab-as-orchestrator (Decision 13).
- **Clone repos**: Not applicable to our workflow.

---

## Category 4: The Big Unsolved Question

| Insight | Likes | Author | Key quote / concept |
|---------|------:|--------|-------------------|
| **Continual Learning** | 925 | @VictorTaelin | "Only continual learning is what's missing. Agents and memory markdowns are insufficient due to information loss." |
| **Context rot** | 1,861 | @AnishA_Moonka | GPT-5.4 loses 54% retrieval at 1M tokens. Opus 4.6 loses only 15%. |

### Our position:
VictorTaelin's observation is exactly our experience. Memory markdowns (CLAUDE.md, STATUS.json, MEMORY.md) are necessary but insufficient. They capture *what* but lose *why* and *how we decided*. The SESSION_ARCHIVE.md we built today is an attempt to bridge this gap — preserving the reasoning and decision history, not just the current state.

The context rot data is encouraging for our approach: Opus 4.6's 15% loss at 1M tokens means that larger context windows might eventually make some of our session boundary management unnecessary. But we're not there yet.

---

## Summary: What We Use vs. What's Available

| Our Approach | Community Alternative | Status |
|-------------|----------------------|--------|
| STATUS.json | state.md, theorist layer | Similar concepts, ours is machine-readable |
| MEMORY.md (manual) | Auto-Memory, Claude-Mem | Should evaluate auto-memory |
| SESSION_ARCHIVE.md | QMD, sync-claude-sessions | Similar goal, different implementation |
| Pre-compact hook | Ralph Wiggum loop | Simpler version of the same idea |
| Code-tab orchestrator | Handoff skills, delegation docs | We evolved past delegation (Decision 13) |
| digest_sessions.py | Smart Forking /fork-detect | Different approach, similar goal |

### Key question for README:
We should acknowledge that community solutions exist and explain *why* we chose our approach: we prioritize understanding what works before adopting, and we value approaches that are transparent and inspectable over opaque plugins. Our "watch-then-adopt" principle means we intentionally lag behind the bleeding edge.

---

*This review should be refreshed after each bookmark fetch to capture new community developments.*

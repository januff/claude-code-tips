# Claude Code Tips

A curated collection of 109 tips from the Claude Code community—and a **live demonstration** of multi-instance Claude workflows.

## What Makes This Repo Different

This isn't just a tips list. It's an experiment in **coordinating multiple Claude instances** on a shared codebase:

- **Claude Code CLI** created the initial structure
- **Cursor Sidebar (Opus 4.5)** reviewed and critiqued plans
- **Claude Desktop App** refined the integration strategy
- **Claude Mobile App** completed atomic tasks from bed

The repo documents the tips *and* demonstrates the best practices they describe—particularly **Tip #1: The Handoff Technique**.

---

## Source Material

**Original Thread:** [Twitter/X post by @alexalbert__](https://x.com/alexalbert__/status/1873757681803608558) (Anthropic's Claude Relations lead)  
**Posted:** December 26, 2025  
**Engagement:** 98.3K views • 667 likes • 941 bookmarks • 182 replies

---

## Repository Contents

```
claude-code-tips/
├── CLAUDE.md                      # Instructions for Claude instances
├── README.md                      # You are here
├── .gitignore                     # Created by mobile app (Task #001)
│
├── tips/
│   ├── full-thread.md             # Complete 109 tips with formatting
│   ├── grouped-tips.md            # Tips organized by theme
│   └── raw-thread-unformatted.md  # Original raw text (archived)
│
├── analysis/
│   └── claude-commentary.md       # Opus 4.5 analysis and recommendations
│
├── plans/
│   ├── integration-plan.md        # Current plan (v2, amended)
│   ├── mobile-task-001.md         # Example atomic task for handoff
│   └── archive/                   # Historical versions
│       ├── integration-plan-v1.md
│       └── integration-plan-review.md
│
└── .claude/
    └── settings.json              # Claude Code permissions
```

---

## Top Tips by Engagement

| Rank | Tip | Likes | Why It Matters |
|------|-----|-------|----------------|
| 1 | **The Handoff Technique** | 160 | Generate self-contained prompts for handing work between AI instances |
| 2 | **"Take a step back and think holistically"** | 77 | Escape infinite loops with this phrase |
| 3 | **"Threaten to use Codex"** | 53 | Emotional prompting (surprisingly effective) |
| 4 | **Architect in Claude Desktop first** | 52 | Separate planning from implementation |
| 5 | **DevSQL for prompt analysis** | 43 | Analyze your own prompt history with SQL |

---

## Key Themes from 109 Tips

### Context Management (Most Common)
- Clear sessions **proactively**, not when forced
- Use `/compact` before auto-compact triggers
- Store intermediate progress in markdown files
- Use subagents for context isolation

### Planning vs Execution
- Never plan and implement in the same session
- Create detailed plans in `.md` files before coding
- Use Plan Mode (`Shift+Tab`) for exploration

### Documentation as Infrastructure
- `CLAUDE.md` is the foundation—every project needs one
- Treat memory files like code files
- Document for handoff: assume the next reader has zero context

### Extended Thinking
`think` < `think hard` < `think harder` < `ultrathink`  
(Reserve `ultrathink` for architectural decisions only)

---

## Multi-Instance Workflow

This repo is designed for **Claude-to-Claude handoffs**. Here's the pattern we're using:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Planning       │────▶│  Review         │────▶│  Implementation │
│  Instance       │     │  Instance       │     │  Instance       │
│  (Desktop App)  │     │  (Cursor/Other) │     │  (Claude Code)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                               │
         │              ┌─────────────────┐              │
         └─────────────▶│  Mobile App     │◀─────────────┘
                        │  (Atomic Tasks) │
                        └─────────────────┘
```

**Instance Roles:**
- **Planner:** Architecture decisions, prompt generation (read-only exploration)
- **Reviewer:** Critique plans, check for gaps, suggest amendments
- **Implementer:** Execute approved plans, make code changes
- **Mobile:** Lightweight atomic tasks, away-from-desk review

See `plans/integration-plan.md` for the full workflow documentation.

---

## Progress: Phase 1 (Foundation)

| Task | Status | Completed By |
|------|--------|--------------|
| Update CLAUDE.md structure | ⏳ Pending | — |
| Code word verification | ✅ Done | Pre-existing |
| Create .gitignore | ✅ Done | Mobile App |
| Add LICENSE | ⏳ Pending | — |

---

## Roadmap (Phases 2-4)

**Phase 2: Structural Scaffolding**
- [ ] `configs/starter-claude-md.md` — Template for new projects
- [ ] `configs/example-hooks.json` — Hook configuration examples
- [ ] `skills/context-management/SKILL.md` — Context management skill
- [ ] `lessons/learning-plan.md` — 4-week learning curriculum

**Phase 3: Multi-Instance Infrastructure**
- [ ] `plans/handoff-template.md` — Standardized handoff format
- [ ] `docs/instance-roles.md` — Role definitions and responsibilities

**Phase 4: Self-Sustaining Agent (Future)**
- [ ] Chrome extension workflow for tip collection
- [ ] Automated tip integration pipeline
- [ ] Community contribution flow

---

## For Humans

Browse [`tips/full-thread.md`](tips/full-thread.md) for all 109 tips, or [`tips/grouped-tips.md`](tips/grouped-tips.md) for thematic organization. The [`analysis/claude-commentary.md`](analysis/claude-commentary.md) file has Opus 4.5's take on which tips matter most.

## For Claude Instances

Read [`CLAUDE.md`](CLAUDE.md) first—it contains project instructions and the verification code word. New Claude Code sessions in this directory will automatically load it.

## Contributing

Found a great Claude Code tip? Open an issue or PR with:
- The tip itself
- Source/attribution (Twitter handle, link)
- Your experience using it

---

## License

MIT — use freely, attribution appreciated.

---

*This repository demonstrates multi-instance Claude workflows. It was created through collaboration between Claude Code, Cursor Sidebar, Claude Desktop, and Claude Mobile—December 26-27, 2025.*

# A/B Test Findings — 2026-04-19

> Experiment: trimmed vs. bloated CLAUDE.md, evaluated by two cold-start
> subagents executing (1) orientation and (2) `/fetch-bookmarks` execution plan.
> Result: trimmed performs equivalently. Cuts applied in same commit as this file.

## Top-line result

| Dimension | Bloated (8,542 bytes) | Trimmed (3,927 bytes) |
|-----------|----------------------:|----------------------:|
| Cold-start self-rated confidence | 7/10 | 7/10 |
| Fetch-bookmarks self-rated confidence | 7/10 | 7/10 |
| Caught "Feb 2026 date directive is stale" | Yes | N/A (cut) |
| Caught "Boris table is trivia, not guidance" | Yes | N/A (cut) |
| Caught STATUS.json `known_issues` drift | No (distracted) | Yes |
| Recovered from skill file staleness | Yes (via MEMORY.md) | Yes (via deferred tool list) |

The trimmed version's removal of bloat *increased* attention to genuine noise elsewhere (STATUS.json drift). The bloated version's extra context helped on one recovery path (MEMORY.md citation) but the trimmed version reached the same conclusion via different evidence.

## Secondary findings surfaced by the A/B test

These weren't in the audit scope but both subagents independently identified them. Flagging for future passes:

### 1. `.claude/commands/fetch-bookmarks.md` has stale content

The skill file (287 lines) still lists Chrome DevTools MCP as the preferred browser backend, but Chrome DevTools MCP was removed from global config on 2026-03-19 in favor of Claude-in-Chrome. Both subagents caught this and worked around it.

**Fix scope:** edit `.claude/commands/fetch-bookmarks.md` to reflect the current browser tooling. Same failure class as the audit's Section 3 finding (stale one-off content) — just in a different file. An audit pass of all `.claude/commands/*.md` files against current reality is warranted.

### 2. Enrichment pipeline has undocumented API key requirements

`enrich_keywords.py`, `enrich_summaries.py`, `enrich_links.py`, `enrich_media.py` all call external LLM APIs (Gemini, summarizer LLM). Neither CLAUDE.md version nor the skill file mentions what API keys are needed or where they're configured. Both subagents had to assume "implicit from prior runs."

**Fix scope:** document env var requirements once, probably in either the skill frontmatter or a dedicated setup section. Not urgent (the keys exist and work), but a future instance might regress without warning.

### 3. STATUS.json should signal "last fetch was today — expect 0 new"

Both subagents had to infer from `last_bookmark_fetch: 2026-04-18` (when today is 2026-04-19 or similar) that a re-run would be low-yield. Making this explicit would reduce cognitive load for every future instance.

**Fix scope:** add a derived field like `fetch_ready: true|false` or a human-readable hint. Or simpler: the Phase 1 summary at start of fetch can compute "days since last fetch" and show it.

## Meta-observation: what CLAUDE.md is actually for

The A/B test revealed something subtle: for deterministic skill execution (like `/fetch-bookmarks`), almost **none of CLAUDE.md matters**. The skill file is self-contained. Both subagents flagged the Research-First Heuristic and Quality-Filtered Export Pattern as noise *for that specific task* — even though those are the audit's gold-standard sections.

This suggests CLAUDE.md's job is:

1. **Orientation** — cold-start shape of the project, cross-project navigation
2. **Discoverability** — where to find things so the instance knows what to reach for
3. **Cross-task principles** — heuristics that apply when no specific skill exists (Research-First)

What CLAUDE.md is **not** for:

- Executing any specific known skill (that's the skill file's job)
- Reference material that's searchable elsewhere (that's `LEARNINGS.md`'s job)
- Architectural history (that's `PROJECT_DECISIONS.md`'s job)
- Operational constraints that change weekly (that's `STATUS.json`'s job)

The trimmed version aligns with this division. The bloated version conflated all four.

## What changed in the swap

Content cut from CLAUDE.md:

- Current Date Awareness directive (stale one-off fix)
- Boris Cherny's Tips table (12 rows of general community reference material)
- Historical note about retired chat-tab delegation (belongs in PROJECT_DECISIONS.md Decision 13)
- Extended Thinking section (generic Claude knowledge)
- Useful Commands section (except `whats_new.py`)
- Cold-Start Prompt template (written for user, not Claude)
- "context-first" verification magic word (attestation-as-instruction)
- Duplicate "Check STATUS.json first" emphasis

Content preserved and/or consolidated:

- STATUS.json-first cold-start rule (merged with "Your Task" decision tree)
- Project purpose and cross-project context
- Code-tab-as-orchestrator model (trimmed to project-specific parts)
- Research-First Heuristic (kept intact — gold standard)
- Claude-in-Chrome contention note (kept, MCP tool list removed)
- Quality-Filtered Export Pattern (kept intact — gold standard)
- Project structure pointer (simplified from tree to 3-line list)
- `whats_new.py` script reference

Result: 239 → 101 lines, 8,542 → 3,927 bytes (~54% reduction in bytes, ~58% in lines).

## Reversibility

The original CLAUDE.md is preserved at `analysis/audits/2026-04-19-CLAUDE_before.md`. To revert:

```bash
cp analysis/audits/2026-04-19-CLAUDE_before.md CLAUDE.md
```

If any regression appears in the next few sessions, identify the specific missing rule that would have prevented it, and add back **only that rule** — not the whole file.

## Follow-ups in priority order

1. **Apply the three A/B test findings** (skill file staleness, API key docs, STATUS.json fetch hint) — each is a small targeted fix.
2. **Run the audit against `.claude/commands/*.md`** — fetch-bookmarks staleness suggests other skill files may have drift.
3. **Run the audit against MEMORY.md** (auto-memory file) — not touched in this pass.
4. **Schedule the next audit** — itsolelehmann's principle is "your AI setup should be getting simpler over time." Set a reminder for ~30 days.

---

*Experiment run by Claude Opus 4.6, 2026-04-19. Audit doc: `2026-04-18-claude-md-audit.md`. Before-state preserved: `2026-04-19-CLAUDE_before.md`.*

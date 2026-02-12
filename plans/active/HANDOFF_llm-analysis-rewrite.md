# HANDOFF: Rewrite analyze_new_tips.py — LLM Classification

> **From:** Claude.ai Planning Instance
> **To:** Claude Code
> **Priority:** High — the current analysis engine is non-functional (34/36 = ACT_NOW)
> **Estimated effort:** 1-2 hours
> **Dependencies:** GOOGLE_API_KEY (Gemini), existing enrichment pipeline patterns

---

## Problem

First live pipeline test (2026-02-11) produced a useless briefing: 34 of 36 tweets classified as ACT_NOW. Three compounding causes:

1. **Keyword lists too broad** — genre terms like "skills", "mcp", "hook" match virtually every Claude Code tip
2. **Substring matching too loose** — PROGRESS.md technique "subagents for parallel work" matches on the 4-letter word "work", hitting 25+ unrelated tweets
3. **Engagement thresholds miscalibrated** — bookmarked tweets are pre-filtered for quality; nearly all exceed the 100-like MEDIUM threshold

**Root cause:** Using string containment to gauge relevance is fundamentally the wrong approach. We have LLM infrastructure — use it.

---

## Solution: Replace Keyword Matching with Gemini Classification

### Architecture

```
For each new tweet:
  1. Load tweet text + enriched summary + author context
  2. Load condensed project context (~500 tokens)
  3. Send single Gemini call requesting structured JSON classification
  4. Parse response into same 4-tier output format

Output format unchanged → generate_briefing.py needs no changes
```

### New file: `.claude/references/project-context-for-analysis.md`

Create a condensed (~500 token) project context document that the analysis script sends as context with each classification call. Content:

```markdown
# Project Context for Tip Analysis

## What we actively use (DO NOT flag as new)
- Delegation pattern: Claude.ai for planning, Claude Code for execution
- Handoff documents for cross-instance communication
- MCP servers (GitHub, filesystem) for tool access
- SQLite as source of truth, Obsidian as read-only export
- Quality-filtered vault export with semantic filenames
- Skills (slash commands) with YAML frontmatter and progressive disclosure
- File-based planning (task_plan.md, STATUS.json)
- Pre-compact and session-end hooks for automatic wrap-up
- Compounding summaries (daily, weekly, goals-audit)

## What we're actively building
- Autonomous daily bookmark monitor (pipeline complete, analysis engine in progress)
- LLM-based tip classification for morning briefings
- Cross-project coordination with hall-of-fake sibling repo

## What we're experimenting with
- Cross-model review (Claude + Codex/Gemini for code critique)
- Obsidian CLI integration (lightweight — vault health checks only)
- Ralph Wiggum for long-running task recovery

## What we've decided to skip
- Beads/Agent Mail (no success stories beyond creator, $550/mo)
- Agent SDK (different use case than archive work)
- Cowork (underwhelming for dev-heavy workflows)
- Voice/STT loops (not our workflow)
- Clawdbot overnight builds (cool demo, wrong fit)

## What matters for classification
- Tips about techniques we already use are NOTED (unless they reveal something new)
- Tips about techniques we're building/experimenting with are EXPERIMENT
- Tips that are genuinely new AND high-signal AND directly applicable are ACT_NOW
- ACT_NOW should be rare (1-3 per batch, not 34)
- Author reputation matters: Boris Cherny, Anthropic staff, high-engagement creators carry more weight
- Engagement is context, not a threshold: 500 likes on a niche technique > 5000 likes on a generic take
```

This file gets updated when LEARNINGS.md or PROGRESS.md changes meaningfully — not on every run.

### Rewrite: `scripts/analyze_new_tips.py`

**Keep:**
- argparse interface (--since, --ids, --output, --dry-run, --db)
- JSON output format (categories dict with ACT_NOW/EXPERIMENT/NOTED/NOISE arrays)
- Entry format per tweet (tweet_id, author, likes, text_preview, category, reason, relevance, proposed_action)
- The `get_new_tweets()` function (DB query is fine)
- Cross-referencing hall-of-fake STATUS.json (pass as context to LLM, not keyword match)

**Remove:**
- All keyword lists (WORKFLOW_KEYWORDS dict)
- All substring matching logic
- `extract_adopted_techniques()`, `extract_pending_techniques()`, `extract_learnings_sections()`
- `classify_tip()` function (replace entirely)
- Hardcoded engagement thresholds

**Add:**
- Load `.claude/references/project-context-for-analysis.md` as context
- Gemini API call per tweet (or batched — see below)
- Structured JSON response parsing with fallback on malformed responses
- `--no-llm` flag that falls back to a simple engagement-only heuristic (for testing without API key)

### Gemini Prompt Design

```
You are classifying a Claude Code tip for a daily briefing. 

PROJECT CONTEXT:
{project_context_contents}

TWEET TO CLASSIFY:
Author: @{handle} ({display_name})
Likes: {likes} | Reposts: {reposts} | Views: {views}
Text: {text}
Summary: {holistic_summary}
Keywords: {keywords_json}
{card_url_if_present}

Classify this tip into exactly one category:
- ACT_NOW: Genuinely new technique that's directly applicable to our active work. Should be rare.
- EXPERIMENT: Interesting technique worth investigating, or relevant to something we're building.
- NOTED: Good to know but no action needed. Includes updates on things we already use.
- NOISE: Low signal for our specific workflow.

Respond in JSON:
{
  "category": "ACT_NOW|EXPERIMENT|NOTED|NOISE",
  "reason": "1-2 sentence explanation of why this classification",
  "relevance": ["specific connections to our project, if any"],
  "proposed_action": "what to do about it, or null"
}
```

### Batching Strategy

Two options — implementer's choice:

**Option A: One call per tweet.** Simplest. ~36 calls for a batch, ~5-10 for daily. Cost: ~$0.01-0.05 per run. Easier to debug, each classification is independent.

**Option B: Batch 5-10 tweets per call.** Fewer API calls, but risk of the model conflating tweets or producing malformed JSON for the batch. Needs more robust parsing.

Recommend Option A for now. Optimize later if cost or latency becomes an issue.

### Rate Limiting

Follow the pattern in `enrich_summaries.py` — the existing enrichment scripts already handle Gemini rate limits. Use the same approach (pause between calls, retry on 429).

### Error Handling

- If Gemini call fails for a tweet, classify as NOTED with reason "classification failed — review manually"
- If response JSON is malformed, attempt to extract category from text, fall back to NOTED
- Log all failures to stderr (pipeline logger captures this)

---

## Verification

After rewrite, re-run on the existing 36-tweet batch:

```bash
python scripts/analyze_new_tips.py --since 2026-02-10
```

Success criteria:
- ACT_NOW should be 0-5 tweets (not 34)
- NOISE should be >0 (some tweets genuinely aren't relevant to us)
- Each "reason" field should demonstrate understanding of the tweet AND the project
- Boris Cherny's Cowork announcement should be NOTED (we decided to skip Cowork)
- @anthonyriera's planning-with-files should be NOTED (we already adopted this in Phase 2)
- @pauloportella_'s pre-compact hook should be NOTED (we already built this in Phase 3)

---

## Also: Fetch the New Bookmarks First

Before testing the rewritten analysis, fetch the bookmarks the user just added:

```bash
claude --chrome
# then: /fetch-bookmarks
```

Expected new tweets: recent posts from Boris Cherny, Lydia Haley, Tariq, and other Anthropic staff within the last 12 hours. After fetch, run the full enrichment pipeline, then test analysis.

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `scripts/analyze_new_tips.py` | Rewrite classification logic |
| `.claude/references/project-context-for-analysis.md` | Create (new) |
| `scripts/generate_briefing.py` | No changes needed (same JSON input format) |
| `scripts/daily_monitor.py` | No changes needed (calls analyze_new_tips.py as subprocess) |

---

*Source: Claude.ai planning review of first live pipeline test, 2026-02-11.*

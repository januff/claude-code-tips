---
name: review-plan
description: >
  Cross-model plan review. Sends the active TASK_PLAN.md (or a specified plan file)
  to a second AI model for adversarial review. Asks: what's missing, what will go wrong,
  what would you do differently. Saves feedback to analysis/reviews/ and then Claude Code
  addresses the feedback. Use before executing a plan to catch blind spots.
argument-hint: [plan-file-path] [reviewer-cli]
---

# Cross-Model Plan Review

Get a second opinion on a plan before executing it.

## Input

- `$ARGUMENTS` — optional path to a plan file (default: `plans/active/TASK_PLAN.md`)
- If a second argument is provided, use it as the reviewer CLI (default: `codex`)

## Workflow

### 1. Detect Reviewer CLI

Same detection as `/review` — check availability:

```bash
which codex 2>/dev/null || which gemini 2>/dev/null || which opencode 2>/dev/null
```

**If no reviewer CLI is found:** Print this message and stop:

```
PLAN REVIEW SKIPPED — No reviewer CLI found.
Install one of: codex, gemini, opencode
See .claude/references/reviewer-cli-guide.md for setup details.
```

### 2. Load Plan

- If a path was provided, read that file
- Otherwise, read `plans/active/TASK_PLAN.md`
- If the plan file doesn't exist, say so and stop

Also load these for context (if they exist):
- `STATUS.json` — current project state
- `LEARNINGS.md` — techniques and conventions (first 100 lines only)

### 3. Send to Reviewer

Use a plan-specific prompt:

```bash
codex -q "You are reviewing a project plan before execution. Analyze it critically:

1. What's missing? (steps, edge cases, dependencies)
2. What will go wrong? (risks, failure modes, unrealistic assumptions)
3. What would you do differently? (better approaches, reordering, scope changes)

Be direct and specific. Don't pad with praise.

PROJECT CONTEXT:
$STATUS_JSON

PLAN:
$PLAN_CONTENT"
```

### 4. Save Review

Write to `analysis/reviews/YYYY-MM-DD-plan-review.md`:

```markdown
# Plan Review: <plan title or filename>
**Date:** YYYY-MM-DD HH:MM
**Reviewer:** <cli-name>
**Plan file:** <path>

---

<reviewer output>
```

### 5. Address Feedback

After saving and displaying the review:

1. Read through each piece of feedback
2. For each point, decide: **accept** (modify the plan), **note** (valid but out of scope), or **disagree** (explain why)
3. Print a response table:

```
FEEDBACK RESPONSE:
  [accept] "Missing error handling for X" — Will add to step 3
  [note]   "Should consider Y" — Valid, tracked for future iteration
  [disagree] "Z is unnecessary" — Needed because [reason]
```

4. If any feedback was accepted, offer to update the plan file

## Notes

- Plan reviews are more valuable BEFORE execution — run this early
- The reviewer gets project context (STATUS.json) to ground its feedback
- Accepted feedback should be incorporated before proceeding with `/task-plan` execution

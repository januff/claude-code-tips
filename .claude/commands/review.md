---
name: review
description: >
  Cross-model code review. Sends a file or git diff to a second AI model (codex, gemini,
  or opencode) for independent review. Checks for correctness, edge cases, missed
  opportunities, and architectural concerns. Saves review to analysis/reviews/.
  Use when you want a second opinion on code, plans, or analysis outputs.
argument-hint: <file-path-or-"diff"> [reviewer-cli]
---

# Cross-Model Review

Review code or plans using an independent AI model.

## Input

- `$ARGUMENTS` — either a file path or the literal word "diff"
- If a second argument is provided, use it as the reviewer CLI (default: `codex`)

## Workflow

### 1. Detect Reviewer CLI

Check availability in this order (use first argument override if provided, otherwise try defaults):

```bash
# Check if the specified (or default) CLI exists
which codex 2>/dev/null || which gemini 2>/dev/null || which opencode 2>/dev/null
```

**If no reviewer CLI is found:** Print this message and stop:

```
REVIEW SKIPPED — No reviewer CLI found.
Install one of: codex, gemini, opencode
See .claude/references/reviewer-cli-guide.md for setup details.
```

### 2. Prepare Review Content

- **If argument is a file path:** Read the file contents
- **If argument is "diff":** Run `git diff HEAD` (staged + unstaged changes)
- **If argument is empty:** Run `git diff --cached` (staged changes only)

### 3. Send to Reviewer

Construct the review prompt and send via the reviewer CLI.

For `codex`:
```bash
codex -q "Review this code for: correctness, edge cases, missed opportunities, and architectural concerns. Be specific — cite line numbers or sections. If everything looks good, say so briefly.

$CONTENT"
```

For `gemini`:
```bash
gemini -q "Review this code for: correctness, edge cases, missed opportunities, and architectural concerns. Be specific — cite line numbers or sections. If everything looks good, say so briefly.

$CONTENT"
```

For `opencode`: use equivalent invocation pattern.

### 4. Save Review

Write the review output to `analysis/reviews/YYYY-MM-DD-<slug>.md`:

```markdown
# Review: <filename or "git diff">
**Date:** YYYY-MM-DD HH:MM
**Reviewer:** <cli-name>
**Input:** <file path or "diff">

---

<reviewer output>
```

Where `<slug>` is derived from the input filename (e.g., `review.md` becomes `review`) or `git-diff` for diff reviews.

### 5. Report

Print the review inline in the conversation, then note where it was saved.

## Notes

- The reviewer runs as a one-shot query — no interactive session
- Review files accumulate in `analysis/reviews/` (append-only, never overwritten)
- Supported CLIs documented in `.claude/references/reviewer-cli-guide.md`

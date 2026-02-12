---
name: wrap-up
description: >
  End-of-session wrap-up that updates STATUS.json with live database stats and latest
  commit info. Use at the end of every Claude Code session. MANDATORY before ending
  any session. Hooks handle automatic wrap-up on compaction and session end.
disable-model-invocation: true
---

# Wrap Up Session

## Hook vs Manual Context

**Manual invocation** (`/wrap-up`): Full wrap-up — plan check, recent_changes updates, commit.

**Automatic (hooks)**: The pre-compact and session-end hooks run `wrap-up-script.py` directly.
They skip the plan check and recent_changes updates to stay lightweight. If you know
compaction is about to happen and want a full wrap-up, run `/wrap-up` manually first.

## Active Plan Check

If `plans/active/TASK_PLAN.md` exists:
1. Read it and note progress against the plan
2. Update the Progress Log table with work done this session
3. Update `active_task.current_phase` in STATUS.json if the phase changed

## Run Wrap-Up Script

```bash
python .claude/references/wrap-up-script.py
```

Then stage and commit:

```bash
git add STATUS.json
git commit -m "chore: wrap-up — update STATUS.json"
```

## When to Update `recent_changes`

If you made substantive changes this session (new features, bug fixes, data operations), update the `recent_changes` array in STATUS.json BEFORE the wrap-up commit. Keep to 5-7 items, removing oldest entries as new ones are added.

## When to Update `known_issues`

If you fixed a known issue, remove it. If you discovered a new one, add it.

## When to Update `key_dates`

Update `last_bookmark_fetch` after `/fetch-bookmarks`. Update `last_vault_export` after running `export_tips.py`.

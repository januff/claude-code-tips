---
name: task-plan
description: >
  Create a file-based task plan for a multi-step task. Use when starting any non-trivial
  work that spans multiple steps or sessions. Creates plans/active/TASK_PLAN.md and
  updates STATUS.json. Re-read the plan after every major step to stay on track.
argument-hint: <description of the task to plan>
---

# Create Task Plan

## Workflow

1. **Check for existing plan** — if `plans/active/TASK_PLAN.md` exists, ask whether to archive it or resume it
2. **Read the template** at `.claude/references/plan-template.md`
3. **Create `plans/active/TASK_PLAN.md`** by filling in the template with:
   - Clear goal derived from `$ARGUMENTS`
   - Concrete success criteria (testable, not vague)
   - Numbered steps broken into phases
   - Known risks and mitigation strategies
4. **Update STATUS.json** — set `active_task` field:
   ```json
   "active_task": {
     "plan": "plans/active/TASK_PLAN.md",
     "description": "<one-line summary>",
     "current_phase": "Phase 1: <name>"
   }
   ```
5. **Present the plan** for user review before executing

## During Execution

- **Re-read `plans/active/TASK_PLAN.md` after every major step** — this is the core pattern
- Update the Progress Log table as steps complete
- Check off success criteria as they are met
- If the plan needs to change, update it (plans are living documents)
- Update `active_task.current_phase` in STATUS.json when moving between phases

## On Completion

1. Mark all success criteria as checked
2. Update status line to `> Status: COMPLETE`
3. Archive: `mv plans/active/TASK_PLAN.md plans/archive/YYYY-MM-DD-task-name.md`
4. Remove `active_task` from STATUS.json
5. Commit the archive move

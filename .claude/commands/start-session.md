---
name: start-session
description: >
  Identify the current starting point for work across all projects and offer options.
  Use at the beginning of any Claude Code session to orient and pick up where the
  last session left off.
disable-model-invocation: true
---

# Start Session

Scan repos for current state and present the starting point.

## Steps

1. **Read STATUS.json** for last session state
2. **Check for active handoffs:** `plans/active/HANDOFF*.md`
3. **Read latest git log** for recent commits
4. **Validate against live filesystem** — is the identified task still relevant?
5. **Present starting point** with options

## Expected Output

```
STARTING POINT IDENTIFIED

Based on: [source — e.g., "HANDOFF.md in claude-code-tips"]
Last updated: [date]

> "[The identified task]"

Verified: [validation result]

REFRESH OPTION
Last fetch: [X days ago]
[1] Work on identified task
[2] Refresh first, then work on task
[3] Refresh only (fetch/enrich/export cycle)

Which approach?
```

## Cross-Repo Paths

- Hall of Fake: `../Hall of Fake/`
- claude-sessions: `../claude-sessions/`

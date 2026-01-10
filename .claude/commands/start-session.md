# Start Session

Identify the current starting point for work across all projects and offer options.

**Canonical source:** This command is maintained in `claude-sessions` repo. This is a copy for convenience.

## Usage

```
/start-session
```

No arguments needed — the command figures out what to do.

## What This Command Does

1. **Scans all three repos** for current state
2. **Identifies the most recent directive** from HANDOFFs or session logs
3. **Validates against live filesystem** (is the bug still there? did the fetch already happen?)
4. **Presents the starting point** for confirmation
5. **Offers a refresh option** (fetch → enrich → update DB) as alternative

## Expected Output

```
📍 STARTING POINT IDENTIFIED

Based on: [source - e.g., "HANDOFF.md in claude-code-tips"]
Last updated: [date]

→ "[The identified task]"

✓ Verified: [validation result]

📊 REFRESH OPTION
Last fetch: [X days ago]
• Twitter: [count] tweets, ready to check for new
• Sora: [count] videos, ready to check for new

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1] Work on identified task
[2] Refresh first → then work on task  
[3] Refresh only (fetch/enrich/export cycle)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Which approach?
```

## Cross-Repo Paths

From this repo (claude-code-tips):
- Hall of Fake: `../Hall of Fake/`
- claude-sessions: `../claude-sessions/`

## Full Implementation

See `.claude/commands/start-session.md` in the `claude-sessions` repo for the complete implementation details.

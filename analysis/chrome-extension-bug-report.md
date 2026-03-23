# Claude-in-Chrome Extension Connection Bug Report (Draft)

> Drafted 2026-03-09 for submission to anthropics/claude-code GitHub issues

---

## Title: Chrome extension "connected but no tabs" loop after multiple sessions — requires 3+ Chrome restarts, never recovers

## Environment

- **Claude Code version:** (check with `claude --version`)
- **Chrome extension version:** 1.0.52
- **OS:** macOS 14.6 (Darwin 23.6.0)
- **Chrome:** (version shown in chrome://version)
- **Claude Desktop also installed:** Yes
- **Claude Code context:** Scheduled task (autonomous, no user at keyboard)

## Symptoms

### Phase 1: Initial connection failure
1. Scheduled task starts, calls `tabs_context_mcp` with `createIfEmpty: true`
2. Returns: "Claude in Chrome is not connected"
3. User restarts Claude Desktop app — no change
4. "Check your Claude in Chrome account" dialog appears on every retry

### Phase 2: Account dialog loop (3 Chrome restarts)
5. Extension settings verified: signed in, correct account, permissions correct, sites approved
6. Clicked "Restart Chrome" from the dialog — connection still fails
7. Second Chrome restart — same result
8. Third Chrome restart — `tabs_context_mcp` returns "connected"

### Phase 3: Connected but stuck
9. `tabs_context_mcp` returns: "The Chrome extension just connected. Retry the tool call now."
10. Retrying returns the same message — indefinitely
11. `tabs_create_mcp` also returns the same "just connected, retry" message
12. **Never progresses to returning actual tab data**
13. Five consecutive calls all return the same "retry" message

### Additional context
- Four other Claude Code terminal sessions had been running earlier (all closed before troubleshooting)
- Colored tab group borders from previous sessions persisted in Chrome (cosmetic only)
- The extension Options page shows correct account ([redacted]) with approved sites (x.com, sora.chatgpt.com)
- This pattern recurs across sessions — not a one-time failure

## Impact

- **Three repositories** depend on this Chrome integration for daily automated bookmark fetching
- **Scheduled tasks** (autonomous, no user interaction) cannot recover from this — there is no mechanism to restart Chrome programmatically
- The "restart Chrome" workaround is not viable for autonomous workflows
- Total time spent troubleshooting this single connection attempt: ~20 minutes + 3 Chrome restarts + 1 Claude Desktop app restart

## Expected behavior

- `tabs_context_mcp` should return tab data after reporting "connected"
- If connection state is stale from previous sessions, it should be cleared automatically
- Scheduled/autonomous tasks should either connect reliably or fail fast with a clear error

## Actual behavior

- Extension enters an intermediate state ("connected" but no tab data) that never resolves
- The "Check your Claude in Chrome account" dialog appears even when the account is correct
- Multiple Chrome restarts are required just to move past the dialog phase
- Once past the dialog, the "retry" loop is a separate, unrecoverable failure mode

## Likely related issues

- #20298 — Master connection failure issue (42 comments, oncall label)
- #32132 — "Check your Claude in Chrome account" dialog (filed Mar 8)
- #27619 — CLI holds stale unix socket after native host restart
- #24593 — "Invalid token or user mismatch" bridge rejection
- #28013 — Permanent disconnect with exponential backoff loop
- #25956 — WebSocket bridge drops and never reconnects

## Suggested improvements

1. **Stale connection cleanup:** Clear previous session state when a new Claude Code instance connects
2. **Fail-fast for autonomous contexts:** If connection can't be established within 30 seconds, return a clear error instead of looping
3. **Native host conflict detection:** Detect when Claude Desktop's native host config shadows Claude Code's, and warn the user
4. **Health check after "connected":** Verify tab data can actually be retrieved before reporting connected
5. **Auto-reconnect:** Implement heartbeat monitoring and automatic reconnection when the bridge drops

## Workarounds tried

| Workaround | Result |
|-----------|--------|
| Close all other Claude Code sessions | No effect |
| Restart Claude Desktop app | No effect |
| Restart Chrome (x3) | Moved past dialog, but stuck in retry loop |
| `switch_browser` tool | "No browser responded within timeout" |
| Verify extension settings/account | All correct, no actionable issue found |

## Reproduction steps

1. Use Claude-in-Chrome across multiple Claude Code sessions over several hours
2. Close all sessions
3. Start a new session (or scheduled task) and attempt to connect
4. Observe the "Check your Claude in Chrome account" dialog
5. Restart Chrome and retry — observe the "connected but retry" loop

---

*This report was drafted by Claude Code based on direct observation of the failure during a scheduled task run on 2026-03-09.*
